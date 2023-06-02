import os

from src.config import Config


def pc_abs_paths() -> list[str]:
    """
    Lists all the absolute paths of the point clouds in the point cloud directory.
    :return:
    """
    return [
        os.path.join(Config.RAW_PC_DIR.value, file) for file in os.listdir(Config.RAW_PC_DIR.value) if file.endswith('.las')
    ]

