import os
from dataclasses import dataclass

import open3d as o3d

from src.config import Config
from src.logging.logger import Logger
from src.modules.point_cloud import PointCloud
from src.modules.shapefile import Shapefile
from src.utils.utils import pcd_file_names


@dataclass
class Main:
    """
    Main class of the program
    """

    @staticmethod
    def run() -> None:
        """
        Main function of the program
        :return:
        """
        if Config.CLEAR_PROCESSED_PC.value:
            # Clearing processed point cloud directory if any .las files exists
            if [file for file in os.listdir(Config.PROCESSED_PC_DIR.value) if file.endswith('.las')]:
                Logger.log(__file__).info("Clearing processed point cloud directory")
                [
                    os.remove(
                        os.path.join(Config.PROCESSED_PC_DIR.value, file)
                    ) for file in os.listdir(Config.PROCESSED_PC_DIR.value) if file.endswith('.las')
                ]

        file_names = pcd_file_names()
        [Main.pc_script(file_name=file_name) for file_name in file_names]  # Run script for each point cloud

    @staticmethod
    def pc_script(file_name: str) -> None:
        """
        Script for processing a single point cloud
        :param file_name:
        :return:
        """
        las_path = os.path.join(Config.RAW_PC_DIR.value, file_name + ".las")
        shp_path = os.path.join(Config.SHP_DIR.value, "speedbump_data_xy.shp")

        if not os.path.exists(las_path):
            raise FileNotFoundError(f"Point cloud {las_path} not found")

        if not os.path.exists(shp_path):
            raise FileNotFoundError(f"Shapefile {shp_path} not found")

        pcd = PointCloud.create(file_path=las_path)  # Creating point cloud object
        gdf = Shapefile.create(file_path=shp_path)  # Creating geo-dataframe object

    @staticmethod
    def __test_pre_processing(pcd: o3d.geometry.PointCloud) -> None:
        """
        Tests the pre-processing of a point cloud
        :param pcd:
        :return:
        """
        Logger.log(__file__).info("Testing pre-processing")
        pcd = PointCloud.pre_process(pcd=pcd)
        PointCloud.display(pcd)

    @staticmethod
    def __test_detection(pcd: o3d.geometry.PointCloud) -> None:
        """
        Tests the detection of a point cloud
        :return:
        """
        Logger.log(__file__).info("Testing detection")
        pcd = PointCloud.pre_process(pcd=pcd)
        # PointCloud.display(pcd)
        pcd = PointCloud.detect(pcd=pcd)
        PointCloud.save(pcd=pcd, filename="marked_point_cloud")


if __name__ == "__main__":
    Main.run()
