import os

from src.config import Config
from src.logging.logger import Logger
from src.modules.point_cloud import PointCloud
from src.utils.utils import pcd_file_names


def pc_script(file_name: str) -> None:
    """
    Script for processing a single point cloud
    :param file_name:
    :return:
    """
    las_path = os.path.join(Config.RAW_PC_DIR.value, file_name + ".las")
    shp_path = os.path.join(Config.SHP_DIR.value, file_name + ".shp")

    if not os.path.exists(las_path):
        raise FileNotFoundError(f"Point cloud {las_path} not found")

    if not os.path.exists(shp_path):
        raise FileNotFoundError(f"Shapefile {shp_path} not found")

    pcd = PointCloud.create(file_path=las_path)  # Creating point cloud object
    pcd = PointCloud.pre_process(pcd=pcd)  # Processing point cloud

    segments = PointCloud.test_pcd(pcd)  # Testing point cloud
    Logger.log(__file__).info(f"Number of segments: {len(segments)}")
    pcds = [segment.pcd for segment in segments]
    PointCloud.display(pcd)
    PointCloud.display(*pcds)


def main() -> None:
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
    [pc_script(file_name=file_name) for file_name in file_names]  # Run script for each point cloud


if __name__ == "__main__":
    main()
