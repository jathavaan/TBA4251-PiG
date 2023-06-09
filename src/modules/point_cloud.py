import math
import os
import uuid

import laspy
import numpy as np
import open3d as o3d
import pandas as pd
from open3d.cpu.pybind.geometry import PointCloud
from tqdm import tqdm

from ..config import Config
from ..logging import logger
from ..modules import Plane
from ..utils import df_to_pcd, pcd_to_df, indexes_to_pcd, pcd_to_plane, create_df


class PointCloud:
    @staticmethod
    def create(file_path: str) -> o3d.geometry.PointCloud:
        """
        Creates a point cloud object from a .las file.
        :param file_path: Path to .las file
        :return: Point cloud object
        """
        if file_path is None:
            raise ValueError("Path is None")

        if not file_path:
            raise ValueError("Path is empty")

        if not file_path.endswith(".las"):
            raise ValueError("Path does not end with .las")

        logger.info(f"Creating point cloud from {file_path}")
        with laspy.open(file_path) as f:
            las = f.read()  # Reading file and creating laspy object

        logger.info(f"Point format: {las.point_format.id}")
        logger.info(f"No. points: {len(las.points)}")
        logger.info(f"Dimensions: {', '.join([name for name in las.point_format.dimension_names])}")

        # Creating dataframe
        rel_intensity = las.intensity / np.max(las.intensity)  # Normalizing intensity
        point_df = create_df(
            X=las.X, Y=las.Y, Z=las.Z, intensity=rel_intensity
        )  # Dataframe with coordinates and intensity

        return df_to_pcd(df=point_df)  # Creating point cloud object

    @staticmethod
    def save(pcd: o3d.geometry.PointCloud, filename: str = None) -> None:
        """
        Saves a point cloud object as a .las file.
        :param pcd: Point cloud to be saved
        :param filename: Name of the file, without extension
        :return:
        """
        logger.info("Saving point cloud as .las file")
        filename = uuid.uuid4().hex + ".las" if filename is None else filename + ".las"  # Creating filename
        path = os.path.join(Config.PROCESSED_PC_DIR.value, filename)

        point_df = pcd_to_df(pcd=pcd)  # Converting point cloud to dataframe
        X, Y, Z = point_df['X'].to_numpy(), point_df['Y'].to_numpy(), point_df['Z'].to_numpy()
        intensity = point_df['intensity'].to_numpy() * 255  # De-normalizing intensity

        header = laspy.LasHeader(point_format=2, version="1.2")  # Creating header
        las = laspy.LasData(header=header)  # Creating laspy object
        las.X, las.Y, las.Z = X, Y, Z  # Adding coordinates
        las.red, las.green, las.blue = intensity, intensity, intensity  # Adding intensity
        las.write(path)  # Writing file
        logger.info(f"Point cloud saved at {path}")
        logger.info(
            f"The following information was saved: {', '.join([name for name in las.point_format.dimension_names])}"
        )

    @staticmethod
    def display(*pcd: o3d.geometry.PointCloud, show_normals: bool = False) -> None:
        """
        Displays a point cloud object.
        :param show_normals: Whether to show normals. Default: False
        :param pcd: Point cloud to be displayed
        :return: None
        """
        if pcd is None or any(p is None for p in pcd):
            raise ValueError("Point cloud is None")

        logger.info("Displaying point cloud")
        if any(len(p.points) == 0 for p in pcd):
            logger.warning("Point cloud is empty")

        o3d.visualization.draw_geometries(pcd, point_show_normal=show_normals)  # Displaying point cloud
        logger.info("Visualisation window closed")

    @staticmethod
    def merge(*pcd) -> o3d.geometry.PointCloud:
        """
        Merges point clouds.
        :param pcd: Point clouds to be merged
        :return: Merged point cloud
        """
        if pcd is None:
            raise ValueError("Point cloud is None")

        merged_df = pd.DataFrame(columns=['X', 'Y', 'Z', 'intensity'])

        for i in tqdm(range(len(pcd)), desc="Merging point clouds", ncols=Config.LOADING_BAR_LENGTH.value):
            df = pcd_to_df(pcd=pcd[i])  # Converting point cloud to dataframe
            merged_df = pd.concat([merged_df, df], ignore_index=True)  # Merging dataframes

        # Removing duplicates and keeping the ones with the highest intensity
        merged_df = merged_df.sort_values(by=['X', 'Y', 'Z', 'intensity'], ascending=[False, False, False, True])
        merged_df = merged_df.drop_duplicates(subset=['X', 'Y', 'Z'], keep='first')

        return df_to_pcd(df=merged_df)  # Converting merged dataframe to point cloud

    @staticmethod
    def inlier_outlier_comparison(
            inlier_pcd: o3d.geometry.PointCloud,
            outlier_pcd: o3d.geometry.PointCloud
    ) -> tuple[o3d.geometry.PointCloud, o3d.geometry.PointCloud]:
        """
        Compares inlier and outlier point clouds.
        :param inlier_pcd:
        :param outlier_pcd: Colors the outlier point cloud red
        :return: Tuple of inlier and outlier point clouds
        """
        outlier_pcd.paint_uniform_color([1, 0, 0])  # Coloring outlier point cloud red
        return inlier_pcd, outlier_pcd

    @staticmethod
    def pre_process(pcd: o3d.geometry.PointCloud) -> o3d.geometry.PointCloud:
        """
        Processing of point cloud. The following happens in this function:
        - Uniform down sampling
        - Statistical outlier removal
        - Middle line point removal (not implemented)
        :param pcd: A raw point cloud
        :return: A processed point cloud
        """
        start_points = len(pcd.points)
        logger.info("Pre-processing point cloud")
        pcd = PointCloud.__uniform_down_sample(pcd=pcd)
        pcd = PointCloud.__statistical_outlier_removal(pcd=pcd)

        """
        This does not work. See the report for more information about why
        gdf = Shapefile.create(file_path=Config.SHAPEFILE_PATH.value)  # Creating shapefile
        pcd = Shapefile.crop(gdf=gdf, pcd=pcd)  # Cropping point cloud
        """

        logger.info(
            f"Point cloud reduced to {len(pcd.points)} points (removed {start_points - len(pcd.points)} points)"
        )

        return pcd

    @staticmethod
    def detect(pcd: o3d.geometry.PointCloud) -> o3d.geometry.PointCloud:
        """
        Detects speed bumps in the segments
        :param pcd: The point cloud that we want to detect speed bumps in
        :return:
        """
        segments = PointCloud.__segment(pcd=pcd)  # Segmenting point cloud
        processed_pcds = []
        detection_count = 0

        for i in tqdm(range(len(segments)), desc="Detecting speed bumps", ncols=Config.LOADING_BAR_LENGTH.value):
            segment = segments[i]

            # Checking parameter
            if Config.MIN_DIST_STD.value < segment.dist_std < Config.MAX_DIST_STD.value \
                    and Config.MIN_ANGLE_DEV.value < segment.mean_angle_dev < Config.MAX_ANGLE_DEV.value:
                logger.debug(
                    f"Segment {i + 1} may contain a speed bump with a standard deviation of {segment.dist_std}"
                    f"and the average deviation from the normal vector of "
                    f"{np.mean(segment.norm_vec_devs)} degrees"
                )

                # Marking points that are part of a speed bump
                df = pcd_to_df(segment.pcd)
                df['intensity'] = 0.0  # Setting intensity to 0
                marked_pcd = df_to_pcd(df=df)

                processed_pcds.append(marked_pcd)
                detection_count += 1
            else:
                processed_pcds.append(segment.pcd)

        logger.info(
            f"Found {detection_count} speed bumps" if detection_count > 0 else "No speed bumps found"
        )
        return PointCloud.merge(*processed_pcds)

    @staticmethod
    def __voxel_down_sample(pcd: o3d.geometry.PointCloud) -> o3d.geometry.PointCloud:
        """
        Downsamples a point cloud object.
        :param pcd: Point cloud to be down sampled
        :return: Down sampled point cloud
        """
        logger.info(f"Downsampling point cloud with voxel size {Config.VOXEL_SIZE.value}...")
        downpcd = pcd.voxel_down_sample(voxel_size=Config.VOXEL_SIZE.value)
        logger.info(f"Downsampled point cloud has {len(downpcd.points)} points")

        return downpcd

    @staticmethod
    def __uniform_down_sample(pcd: o3d.geometry.PointCloud) -> o3d.geometry.PointCloud:
        """
        Downsamples a point cloud object using uniform down sampling
        :param pcd:
        :return:
        """
        logger.debug(f"Downsampling point cloud with every {Config.UNIFORM_DOWN_SAMPLE.value}th point...")
        downpcd = pcd.uniform_down_sample(every_k_points=Config.UNIFORM_DOWN_SAMPLE.value)
        logger.debug(f"Downsampled point cloud has {len(downpcd.points)} points")

        return downpcd

    @staticmethod
    def __statistical_outlier_removal(pcd: o3d.geometry.PointCloud) -> o3d.geometry.PointCloud:
        """
        Removes statistical outliers from a point cloud object
        :param pcd:
        :return:
        """
        logger.debug("Removing statistical outliers...")
        cd, inlier_indexes = pcd.remove_statistical_outlier(
            nb_neighbors=Config.SOR_NO_NEIGHBOURS.value,
            std_ratio=Config.SOR_STD_RATIO.value
        )  # Removing statistical outliers
        logger.debug(f"Point cloud reduced to {len(inlier_indexes)} points")
        downpcd = indexes_to_pcd(pcd=pcd, indexes=inlier_indexes)  # Creating point cloud from inlier indexes

        return downpcd

    @staticmethod
    def __segment(pcd: o3d.geometry.PointCloud) -> list[Plane]:
        """
        Segments a point cloud using basic principles for overlapping areas from photogrammetry
        :param pcd:
        :return: Returns a list of plane objects
        """
        logger.info("Segmenting point cloud...")
        pcd_df = pcd_to_df(pcd=pcd)  # Converting point cloud to dataframe
        total_points = len(pcd_df)  # Total number of points in point cloud
        segment_size = int(total_points / Config.NO_SEGMENTS.value)  # Size of each segment
        overlap_size = int(segment_size * Config.OVERLAP_PERCENTAGE.value)  # Size of overlap between segments

        # Calculating no of iterations required to segment point cloud
        N = math.ceil(np.divide(total_points - segment_size, segment_size * (1 - Config.OVERLAP_PERCENTAGE.value)) + 1)

        start_index = 0  # Start index of segment
        segment_list = []  # List of segments

        for _ in range(N):
            end_index = start_index + segment_size  # End index of segment

            if start_index >= total_points:
                logger.warning("Start index exceeds total number of points")

            # Adjusting end index if it exceeds the total number of points
            if end_index >= total_points:
                end_index = total_points - 1

            segment = pcd_df.iloc[start_index:end_index + 1]  # Segment of point cloud
            segment_list.append(segment)

            start_index = end_index - overlap_size  # Adjusting start index for next segment

        segments = []  # List of segmented point clouds and planes
        for i in tqdm(range(len(segment_list)), desc="Segmenting point cloud", ncols=Config.LOADING_BAR_LENGTH.value):
            segment = segment_list[i]  # Segment of point cloud
            segment_pcd = df_to_pcd(df=segment)  # Converting segment to point cloud
            segment_pcd = PointCloud.__statistical_outlier_removal(pcd=segment_pcd)  # Performing another SOR
            plane = pcd_to_plane(segment_pcd)  # Plane of segment
            segments.append(plane)

        return segments

    @staticmethod
    def __color_pcd(pcd: o3d.geometry.PointCloud, color: list) -> o3d.geometry.PointCloud:
        """
        Marks the point cloud with the detected speed bumps
        :return:
        """
        if len(color) != 3:
            raise ValueError("Color must be a list of length 3")

        if any(c > 1 or c < 0 for c in color):
            raise ValueError("Color values must be between 0 and 1")

        pcd.paint_uniform_color(color)  # Coloring point cloud gray
        return pcd
