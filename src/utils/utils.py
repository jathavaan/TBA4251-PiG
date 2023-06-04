import os

import pandas as pd

from src.config import Config


def pcd_file_names() -> list[str]:
    """
    Lists all the absolute paths of the point clouds in the point cloud directory.
    :return:
    """
    return [
        os.path.splitext(file)[0] for file in os.listdir(Config.RAW_PC_DIR.value) if
        file.endswith('.las')
    ]


def create_df(**cols) -> pd.DataFrame:
    """
    Generates a dataframe from any amount of columns
    :param cols:
    :return:
    """
    df = pd.DataFrame()
    for col_name, col in cols.items():
        df[col_name] = col

    return df
