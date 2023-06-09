from dataclasses import dataclass

import fiona
import geopandas as gpd
from shapely.geometry import shape

from src.logging.logger import Logger
from src.utils.conversion_utils import gdf_to_cartesian_gdf


@dataclass
class Shapefile:
    @staticmethod
    def create(file_path: str) -> gpd.GeoDataFrame:
        """
        Creates a shapefile object and converts the coordinates to Cartesian coordinates
        :param file_path: Path to shapefile
        :return: Shapefile object
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

            crs = shp.crs

        Logger.log(__file__).info(f"Removed {invalid_feature_count} invalid features from shapefile")

        gdf = gpd.GeoDataFrame.from_features(valid_features, crs='EPSG:32632')
        return gdf_to_cartesian_gdf(gdf=gdf)
