import logging
import os
from enum import Enum


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

    # Shapefiles directory paths
    SHP_DIR = os.path.join(RESOURCE_DIR, 'shapefiles')

    # Log directory paths
    LOG_DIR = os.path.join(SOURCE_DIR, 'logging', 'logs')

    # SETTINGS
    # General settings
    LOGGING_LEVEL = logging.INFO  # Logging level
    CLEAR_PROCESSED_PC = True  # Clear processed point cloud directory before processing
    LOADING_BAR_LENGTH = 100  # Length of loading bar

    # Point cloud settings
    # Pre-processing settings
    VOXEL_SIZE = 500  # Voxel size. NB: Not used because uniform down sampling is used
    UNIFORM_DOWN_SAMPLE = 5  # k-nearest neighbour for uniform down sampling
    SOR_NO_NEIGHBOURS = 5  # Number of neighbours for statistical outlier removal (SOR)
    SOR_STD_RATIO = 0.3  # Standard deviation for statistical outlier removal

    # RANSAC plane segmentation settings
    RANSAC_N = 3  # Number of points to sample for RANSAC
    RANSAC_ITER = 1000  # Maximum number of iterations for RANSAC
    RANSAC_THRESH = 60  # Maximum distance for a point to be considered an inlier for RANSAC

    # Normal estimation settings
    SEARCH_RADIUS = 15  # Search radius (in meters) for normal estimation
    MAX_NEAREST_NEIGHBOURS = 100  # Maximum number of nearest neighbours for normal estimation

    # Segmentation settings
    OVERLAP_PERCENTAGE = 0.4  # Percentage of overlap between two segments
    NO_SEGMENTS = 300  # Number of segments to divide PCD into. Should be adjusted according to size of PCD

    # Detection setting
    MIN_DIST_STD = 15.4  # Minimum standard deviation required for a segment to be considered a containing a speedbump
    MAX_DIST_STD = 16.6  # Maximum standard deviation required for a segment to be considered a containing a speedbump
