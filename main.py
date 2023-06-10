import os
from dataclasses import dataclass

from src.config import Config
from src.logging import logger
from src.modules.point_cloud import PointCloud


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
                logger.info("Clearing processed point cloud directory")
                [
                    os.remove(
                        os.path.join(Config.PROCESSED_PC_DIR.value, file)
                    ) for file in os.listdir(Config.PROCESSED_PC_DIR.value) if file.endswith('.las')
                ]

        las_path = Config.POINT_CLOUD_PATH.value
        if not os.path.exists(las_path):
            raise FileNotFoundError(
                f"Point cloud {las_path} not found. "
                f"Make sure the LAS file is in the following directory: {Config.RAW_PC_DIR.value}"
            )

        pcd = PointCloud.create(file_path=las_path)
        pcd = PointCloud.pre_process(pcd=pcd)
        pcd = PointCloud.detect(pcd=pcd)
        PointCloud.display(pcd)
        PointCloud.save(pcd=pcd, filename="marked_point_cloud")


if __name__ == "__main__":
    Main.run()
