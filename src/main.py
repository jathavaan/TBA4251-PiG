import os

import src.utils as utils
from src.config import Config
from src.logging.logger import Logger
from src.modules.point_cloud import create, voxel_down_sample, display
from src.utils.conversion_utils import pcd_to_plane, pcd_abs_paths, indexes_to_pcd


def pc_script(file_path: str) -> None:
    """
    Script for processing a single point cloud
    :param file_path:
    :return:
    """
    pcd = voxel_down_sample(pcd=create(file_path=file_path))  # Create and voxel down sample point cloud
    plane = pcd_to_plane(pcd)
    plane_pcd = indexes_to_pcd(pcd=pcd, indexes=plane.inlier_indexes)

    display(plane_pcd, pcd)


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

    point_cloud_paths = pcd_abs_paths()
    for file_path in point_cloud_paths:
        pc_script(file_path=file_path)


if __name__ == "__main__":
    main()
