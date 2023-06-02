import os
from enum import Enum

import logging


class Config(Enum):
    # PATHS
    # Directory Paths
    ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    SOURCE_DIR = os.path.join(ROOT_DIR, 'src')
    RESOURCE_DIR = os.path.join(ROOT_DIR, 'resources')

    # Point clouds directory paths
    PC_DIR = os.path.join(RESOURCE_DIR, 'point_clouds')
    RAW_PC_DIR = os.path.join(PC_DIR, 'raw_files')
    PROCESSED_PC_DIR = os.path.join(PC_DIR, 'processed_files')

    # Log directory paths
    LOG_DIR = os.path.join(SOURCE_DIR, 'logging', 'logs')

    # SETTINGS
    # General settings
    LOGGING_LEVEL = logging.DEBUG  # Logging level
    CLEAR_PROCESSED_PC = True  # Clear processed point cloud directory before processing

    # Point cloud settings
    # Voxel down sampling settings
    VOXEL_SIZE = 1000  # Voxel size for downsampling

    # RANSAC plane segmentation settings
    RANSAC_N = 3  # Number of points to sample for RANSAC
    RANSAC_ITER = 1000  # Maximum number of iterations for RANSAC
    RANSAC_THRESH = 200  # Maximum distance for a point to be considered an inlier for RANSAC
