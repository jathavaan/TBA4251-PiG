from __future__ import annotations

import geopandas as gpd
import numpy as np
import open3d as o3d
import pandas as pd
import pyproj

from src.config import Config
from ..logging import logger


def df_to_pcd(df: pd.DataFrame) -> o3d.geometry.PointCloud:
    """
    Converts a dataframe to a point cloud object.
    :param df: Dataframe to be converted
    :return: Point cloud object
    """
    logger.debug("Creating point cloud...")
    pcd = o3d.geometry.PointCloud()  # Point cloud object
    pcd.points = o3d.utility.Vector3dVector(np.asarray(df[['X', 'Y', 'Z']]))
    marked_point_indexes = np.where(df['intensity'].to_numpy() == 0.0)  # Marked points
    # TODO: Make the marked color green

    pcd.colors = o3d.utility.Vector3dVector(np.asarray(df[['intensity', 'intensity', 'intensity']]))
    logger.debug(f"Point cloud created with {len(pcd.points)} points")

    return pcd


def pcd_to_df(pcd: o3d.geometry.PointCloud) -> pd.DataFrame:
    """
    Converts a point cloud object to a dataframe.
    :param pcd: Point cloud to be converted, assumes that the point cloud has intensity values
    :return: Dataframe with x, y, z and intensity columns
    """
    logger.debug("Converting point cloud to dataframe...")
    df = pd.DataFrame()
    df['X'] = np.asarray(pcd.points)[:, 0]
    df['Y'] = np.asarray(pcd.points)[:, 1]
    df['Z'] = np.asarray(pcd.points)[:, 2]
    df['intensity'] = np.asarray(pcd.colors)[:, 0]
    logger.debug(f"Point cloud converted to dataframe with {len(df)} rows")

    return df


def indexes_to_pcd(pcd: o3d.geometry.PointCloud, indexes: list[int]) -> o3d.geometry.PointCloud:
    """
    Extracts points from a point cloud object based on the given indexes.
    :param pcd:
    :param indexes:
    :return:
    """
    reduced_pc = pcd.select_by_index(indexes)
    return reduced_pc


def pcd_to_plane(pcd: o3d.geometry.PointCloud) -> Plane:
    """
    Creates a plane from a point cloud. This is done using RANSAC.
    :param pcd: Point cloud to generate plane from
    :return: Plane object
    """
    from ..modules.plane import Plane  # Import here to avoid circular imports

    logger.debug("Generating plane from point cloud")
    plane_model, inlier_indexes = pcd.segment_plane(
        distance_threshold=Config.RANSAC_THRESH.value,
        ransac_n=Config.RANSAC_N.value,
        num_iterations=Config.RANSAC_ITER.value
    )

    pcd = df_to_pcd(pcd_to_df(pcd).loc[inlier_indexes])

    a, b, c, d = plane_model
    plane = Plane(a=a, b=b, c=c, d=d, pcd=pcd)

    return plane


def utm_to_cartesian(gdf: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """
    Converts a geo-dataframe from any coordinate system to cartesian coordinate system.
    :param gdf: Geo-dataframe to be converted
    :return: Geo-dataframe in a cartesian coordinate system
    """
    if gdf is None:
        raise ValueError("Geo-dataframe is None")

    if gdf.crs is None:
        raise ValueError("Geo-dataframe has no coordinate system")

    source_coordinate_system = gdf.crs  # Source coordinate system
    target_coordinate_system = 'EPSG:3857'  # Cartesian coordinate system

    # Transformer object for transformation
    transformer = pyproj.Transformer.from_crs(
        source_coordinate_system,
        target_coordinate_system,  # FIXME: This is not working
        always_xy=True
    )

    gdf['geometry'] = gdf['geometry'].to_crs(transformer.transform)  # Convert geometry column to Cartesian coordinates

    return gdf
