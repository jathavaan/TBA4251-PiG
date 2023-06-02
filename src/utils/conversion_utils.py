import os

import numpy as np
import open3d as o3d
import pandas as pd

from src.config import Config
from src.logging.logger import Logger
from src.modules.plane import Plane


def pcd_abs_paths() -> list[str]:
    """
    Lists all the absolute paths of the point clouds in the point cloud directory.
    :return:
    """
    return [
        os.path.join(Config.RAW_PC_DIR.value, file) for file in os.listdir(Config.RAW_PC_DIR.value) if
        file.endswith('.las')
    ]


def create_df(**cols) -> pd.DataFrame:
    """
    Generates a dataframe from any amount of columns
    :param cols:
    :return:
    """
    df = pd.DataFrame()
    for col_name, col in cols.items():
        df[col_name] = col

    return df


def df_to_pcd(df: pd.DataFrame) -> o3d.geometry.PointCloud:
    """
    Converts a dataframe to a point cloud object.
    :param df: Dataframe to be converted
    :return: Point cloud object
    """
    Logger.log(__file__).info("Creating point cloud...")
    pcd = o3d.geometry.PointCloud()  # Point cloud object
    pcd.points = o3d.utility.Vector3dVector(np.asarray(df[['X', 'Y', 'Z']]))
    pcd.colors = o3d.utility.Vector3dVector(np.asarray(df[['intensity', 'intensity', 'intensity']]))
    Logger.log(__file__).info(f"Point cloud created with {len(pcd.points)} points")

    return pcd


def pcd_to_df(pcd: o3d.geometry.PointCloud) -> pd.DataFrame:
    """
    Converts a point cloud object to a dataframe.
    :param pcd: Point cloud to be converted, assumes that the point cloud has intensity values
    :return: Dataframe with x, y, z and intensity columns
    """
    Logger.log(__file__).info("Converting point cloud to dataframe...")
    df = pd.DataFrame()
    df['X'] = np.asarray(pcd.points)[:, 0]
    df['Y'] = np.asarray(pcd.points)[:, 1]
    df['Z'] = np.asarray(pcd.points)[:, 2]
    df['intensity'] = np.asarray(pcd.colors)[:, 0]
    Logger.log(__file__).info(f"Point cloud converted to dataframe with {len(df)} rows")

    return df


def indexes_to_pcd(pcd: o3d.geometry.PointCloud, indexes: list[int]) -> o3d.geometry.PointCloud:
    """
    Extracts points from a point cloud object based on the given indexes.
    :param pcd:
    :param indexes:
    :return:
    """
    reduced_pc = pcd.select_by_index(indexes)
    reduced_pc.paint_uniform_color([1, 0, 0])
    return reduced_pc


def pcd_to_plane(pcd: o3d.geometry.PointCloud) -> Plane:
    """
    Creates a plane from a point cloud. This is done using RANSAC.
    :param pcd: Point cloud to generate plane from
    :return: Plane object
    """
    Logger.log(__file__).info("Generating plane from point cloud")
    plane_model, inlier_indexes = pcd.segment_plane(
        distance_threshold=Config.RANSAC_THRESH.value,
        ransac_n=Config.RANSAC_N.value,
        num_iterations=Config.RANSAC_ITER.value
    )

    a, b, c, d = plane_model
    plane = Plane(a=a, b=b, c=c, d=d, inliers_indexes=inlier_indexes)

    return plane
