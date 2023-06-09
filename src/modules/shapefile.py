from dataclasses import dataclass

import fiona
import geopandas as gpd
import open3d as o3d
from shapely import Point
from shapely.geometry import shape

from src.config import Config
from src.logging.logger import Logger
from src.utils.conversion_utils import pcd_to_df, df_to_pcd


@dataclass
class Shapefile:
    @staticmethod
    def create(file_path: str) -> gpd.GeoDataFrame:
        """
        Creates a shapefile object and converts the coordinates to Cartesian coordinates
        :param file_path: Path to shapefile
        :return: Geo-dataframe object
        """
        valid_features = []
        invalid_feature_count = 0

        Logger.log(__file__).info(f"Reading shapefile from {file_path}")

        with fiona.open(file_path, 'r') as shp:
            for feature in shp:
                # Removing invalid features
                try:
                    shp_geom = shape(feature['geometry'])
                    if not shp_geom.is_empty:
                        valid_features.append(feature)
                except Exception as e:
                    invalid_feature_count += 1

        if invalid_feature_count > 0:
            Logger.log(__file__).warning(f"Removed {invalid_feature_count} invalid features from shapefile")

        gdf = gpd.GeoDataFrame.from_features(valid_features)  # Create a geopandas dataframe from the valid features
        return gdf

    @staticmethod
    def crop(gdf: gpd.GeoDataFrame, pcd: o3d.geometry.PointCloud) -> o3d.geometry.PointCloud:
        """
        Crops a shapefile to the extent of a point cloud
        :param gdf: Shapefile object
        :param pcd: Point cloud object
        :return: Cropped point cloud
        """
        Logger.log(__file__).info("Cropping point cloud to middle line from shapefile")

        pcd_df = pcd_to_df(pcd=pcd)  # Convert point cloud to dataframe
        for i in range(len(pcd_df)):
            point = Point(pcd_df['X'][i], pcd_df['Y'][i])  # Create a shapely point object
            if gdf.distance(point) > Config.MIDDLE_LINE_THRESHOLD.value:  # Check if point is within shapefile
                pcd_df.drop(i, inplace=True)  # Drop point if not within shapefile

        return df_to_pcd(df=pcd_df)  # Convert dataframe back to point cloud
