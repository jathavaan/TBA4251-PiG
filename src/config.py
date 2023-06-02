import os
from enum import Enum


class Config(Enum):
    # Directory Paths
    ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    RESOURCE_DIR = os.path.join(ROOT_DIR, 'resources')
    PC_DIR = os.path.join(RESOURCE_DIR, 'point_clouds')
    RAW_PC_DIR = os.path.join(PC_DIR, 'raw_files')
    PROCESSED_PC_DIR = os.path.join(PC_DIR, 'processed_files')