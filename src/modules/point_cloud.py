import os
import uuid

import laspy
import numpy as np
import open3d as o3d

from src.config import Config
from src.logging.logger import Logger
from src.modules.plane import Plane
from src.utils.conversion_utils import df_to_pcd, pcd_to_df, indexes_to_pcd
from src.utils.utils import create_df


class PointCloud:
    @staticmethod
    def create(file_path: str) -> o3d.geometry.PointCloud:
        """
        Creates a point cloud object from a .las file.
        :param file_path: Path to .las file
        :return: Point cloud object
        """
        if file_path is None:
            raise ValueError("Path is None")

        if not file_path:
            raise ValueError("Path is empty")

        if not file_path.endswith(".las"):
            raise ValueError("Path does not end with .las")

        Logger.log(__file__).info(f"Creating point cloud from {file_path}")
        with laspy.open(file_path) as f:
            las = f.read()  # Reading file and creating laspy object

        Logger.log(__file__).info(f"Point format: {las.point_format.id}")
        Logger.log(__file__).info(f"No. points: {len(las.points)}")
        Logger.log(__file__).info(f"Dimensions: {', '.join([name for name in las.point_format.dimension_names])}")

        # Creating dataframe
        rel_intensity = las.intensity / np.max(las.intensity)  # Normalizing intensity
        point_df = create_df(X=las.X, Y=las.Y, Z=las.Z,
                             intensity=rel_intensity)  # Dataframe with coordinates and intensity

        return df_to_pcd(df=point_df)  # Creating point cloud object

    @staticmethod
    def save(pcd: o3d.geometry.PointCloud) -> None:
        """
        Saves a point cloud object as a .las file.
        :param pcd:
        :return:
        """
        Logger.log(__file__).info("Saving point cloud as .las file")
        filename = uuid.uuid4().hex + ".las"
        path = os.path.join(Config.PROCESSED_PC_DIR.value, filename)

        point_df = pcd_to_df(pcd=pcd)  # Converting point cloud to dataframe
        X, Y, Z = point_df['X'].to_numpy(), point_df['Y'].to_numpy(), point_df['Z'].to_numpy()
        intensity = point_df['intensity'].to_numpy()

        header = laspy.LasHeader(point_format=2, version="1.2")  # Creating header
        las = laspy.LasData(header=header)  # Creating laspy object
        las.X, las.Y, las.Z = X, Y, Z  # Adding coordinates
        las.red, las.green, las.blue = intensity, intensity, intensity  # Adding intensity
        las.write(path)  # Writing file
        Logger.log(__file__).info(f"Point cloud saved at {path}")
        Logger.log(__file__).info(
            f"The following information was saved: {', '.join([name for name in las.point_format.dimension_names])}"
        )

    @staticmethod
    def display(*pcd: o3d.geometry.PointCloud) -> None:
        """
        Displays a point cloud object.
        :param pcd: Point cloud to be displayed
        :return: None
        """
        if pcd is None:
            raise ValueError("Point cloud is None")

        Logger.log(__file__).info("Displaying point cloud")
        if any(len(p.points) == 0 for p in pcd):
            Logger.log(__file__).warning("Point cloud is empty")

        o3d.visualization.draw_geometries(pcd)
        Logger.log(__file__).info("Visualisation window closed")

    @staticmethod
    def inlier_outlier_comparison(
            inlier_pcd: o3d.geometry.PointCloud,
            outlier_pcd: o3d.geometry.PointCloud
    ) -> tuple[o3d.geometry.PointCloud, o3d.geometry.PointCloud]:
        """
        Compares inlier and outlier point clouds.
        :param inlier_pcd:
        :param outlier_pcd: Colors the outlier point cloud red
        :return: Tuple of inlier and outlier point clouds
        """
        outlier_pcd.paint_uniform_color([1, 0, 0])  # Coloring outlier point cloud red
        return inlier_pcd, outlier_pcd

    @staticmethod
    def process(pcd: o3d.geometry.PointCloud) -> o3d.geometry.PointCloud:
        """
        Processing of point cloud. The following happens in this function:
        - Uniform down sampling
        - Statistical outlier removal
        :param pcd: A raw point cloud
        :return: A processed point cloud
        """
        pcd = PointCloud.__uniform_down_sample(pcd=pcd)
        pcd = PointCloud.__statistical_outlier_removal(pcd=pcd)

        return pcd

    @staticmethod
    def __voxel_down_sample(pcd: o3d.geometry.PointCloud) -> o3d.geometry.PointCloud:
        """
        Downsamples a point cloud object.
        :param pcd: Point cloud to be down sampled
        :return: Down sampled point cloud
        """
        Logger.log(__file__).info(f"Downsampling point cloud with voxel size {Config.VOXEL_SIZE.value}...")
        downpcd = pcd.voxel_down_sample(voxel_size=Config.VOXEL_SIZE.value)
        Logger.log(__file__).info(f"Downsampled point cloud has {len(downpcd.points)} points")

        return downpcd

    @staticmethod
    def __uniform_down_sample(pcd: o3d.geometry.PointCloud) -> o3d.geometry.PointCloud:
        """
        Downsamples a point cloud object using uniform down sampling
        :param pcd:
        :return:
        """
        Logger.log(__file__).info(f"Downsampling point cloud with every {Config.UNIFORM_DOWN_SAMPLE.value}th point...")
        downpcd = pcd.uniform_down_sample(every_k_points=Config.UNIFORM_DOWN_SAMPLE.value)
        Logger.log(__file__).info(f"Downsampled point cloud has {len(downpcd.points)} points")

        return downpcd

    @staticmethod
    def __statistical_outlier_removal(pcd: o3d.geometry.PointCloud) -> o3d.geometry.PointCloud:
        """
        Removes statistical outliers from a point cloud object
        :param pcd:
        :return:
        """
        Logger.log(__name__).info("Removing statistical outliers...")
        cd, inlier_indexes = pcd.remove_statistical_outlier(
            nb_neighbors=Config.SOR_NO_NEIGHBOURS.value,
            std_ratio=Config.SOR_STD_RATIO.value
        )  # Removing statistical outliers
        Logger.log(__name__).info(f"Point cloud reduced to {len(inlier_indexes)} points")
        downpcd = indexes_to_pcd(pcd=pcd, indexes=inlier_indexes)  # Creating point cloud from inlier indexes

        return downpcd

    @staticmethod
    def __segment(pcd: o3d.geometry.PointCloud) -> list[tuple[o3d.geometry.PointCloud, Plane]]:
        """
        Segments a point cloud using KDTree.
        :param pcd:
        :return: Returns a list of point cloud objects and their corresponding planes
        """
        Logger.log(__file__).info("Segmenting point cloud...")
        return None
