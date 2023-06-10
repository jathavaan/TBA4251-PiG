import logging
import os
from enum import Enum


class Config(Enum):
    # CHANGE THESE VALUES TO BE ABLE TO RUN THE PROGRAM
    # Filenames [Without file extension]
    LAS_NAME = "raw_speedbump_data"  # Name of the point cloud file
    SHP_NAME = "speedbump_data_xy"  # Name of the shapefile

    # DO NOT CHANGE THE VALUES BELOW

    # PATHS
    # Directory Paths
    ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    SOURCE_DIR = os.path.join(ROOT_DIR, 'src')
    RESOURCE_DIR = os.path.join(ROOT_DIR, 'resources')

    # Point clouds directory paths
    PC_DIR = os.path.join(RESOURCE_DIR, 'point_clouds')
    RAW_PC_DIR = os.path.join(PC_DIR, 'raw_files')
    PROCESSED_PC_DIR = os.path.join(PC_DIR, 'processed_files')
    POINT_CLOUD_PATH = os.path.join(RAW_PC_DIR, LAS_NAME + '.las')

    # Shapefiles directory paths
    SHP_DIR = os.path.join(RESOURCE_DIR, 'shapefiles')
    SHAPEFILE_PATH = os.path.join(SHP_DIR, SHP_NAME + '.shp')

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

    # RANSAC settings
    RANSAC_N = 3  # Number of points to sample for RANSAC
    RANSAC_ITER = 250  # Maximum number of iterations for RANSAC
    RANSAC_THRESH = 68  # Maximum distance for a point to be considered an inlier for RANSAC (60)

    # Normal estimation settings
    SEARCH_RADIUS = 5  # Search radius (in meters) for normal estimation
    MAX_NEAREST_NEIGHBOURS = 20  # Maximum number of nearest neighbours for normal estimation

    # Segmentation settings
    OVERLAP_PERCENTAGE = 0.1  # Percentage of overlap between two segments (0.4)
    NO_SEGMENTS = 120  # Number of segments to divide PCD into. Should be adjusted according to size of PCD (300)

    # Shapefile pre-processing settings
    MIDDLE_LINE_THRESHOLD = 2  # Maximum distance (meters) between a point and the middle line

    # Detection setting
    MIN_DIST_STD = 13.4  # Minimum standard deviation required for a segment to be considered a containing a speedbump (15.4)
    MAX_DIST_STD = 30  # Maximum standard deviation required for a segment to be considered a containing a speedbump (16.6)
    MIN_ANGLE_DEV = 2  # Minimum deviation in degrees from normal vector of mathematical plane
    MAX_ANGLE_DEV = 10  # Maximum deviation in degrees from normal vector of mathematical plane
