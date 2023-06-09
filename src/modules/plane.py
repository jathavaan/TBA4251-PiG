from dataclasses import dataclass

import numpy as np
import open3d as o3d

from ..config import Config
from ..logging import logger
from ..modules.point import Point
from ..utils import point_plane_dist, vector_angle, pcd_to_df


@dataclass
class Plane:
    __a: float  # x
    __b: float  # y
    __c: float  # z
    __d: float  # Distance from origin
    __pcd: o3d.geometry.PointCloud

    def __init__(
            self, a: float, b: float, c: float, d: float, pcd: o3d.geometry.PointCloud
    ) -> None:
        """
        Constructor for the Plane class
        :param a:
        :param b:
        :param c:
        :param d:
        """
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.pcd = pcd

        logger.debug(f"Plane created with {len(self.__pcd.points)} inliers")

    @property
    def a(self) -> float:
        """
        Getter for a
        :return:
        """
        return self.__a

    @a.setter
    def a(self, a: float) -> None:
        """
        Setter for a
        :param a:
        :return:
        """
        if a is None:
            raise ValueError("a cannot be None")

        self.__a = a

    @property
    def b(self) -> float:
        """
        Getter for b
        :return:
        """
        return self.__b

    @b.setter
    def b(self, b: float) -> None:
        """
        Setter for b
        :param b:
        :return:
        """
        if b is None:
            raise ValueError("b cannot be None")

        self.__b = b

    @property
    def c(self) -> float:
        """
        Getter for c
        :return:
        """
        return self.__c

    @c.setter
    def c(self, c: float) -> None:
        """
        Setter for c
        :param c:
        :return:
        """
        if c is None:
            raise ValueError("c cannot be None")

        self.__c = c

    @property
    def d(self) -> float:
        """
        Getter for d
        :return:
        """
        return self.__d

    @d.setter
    def d(self, d: float) -> None:
        """
        Setter for d
        :param d:
        :return:
        """
        if d is None:
            raise ValueError("d cannot be None")

        self.__d = d

    @property
    def pcd(self) -> o3d.geometry.PointCloud:
        """
        Getter for pcd
        :return:
        """
        return self.__pcd

    @pcd.setter
    def pcd(self, pcd: o3d.geometry.PointCloud) -> None:
        """
        Setter for pcd
        :param pcd:
        :return:
        """
        if pcd is None:
            raise ValueError("pcd cannot be None")

        if len(pcd.points) == 0:
            logger.warning("Point cloud has no points")

        if not isinstance(pcd, o3d.geometry.PointCloud):
            raise TypeError(f"Expected o3d.geometry.PointCloud, got {type(pcd)}")

        self.__pcd = pcd

    def z(self, x: float, y: float) -> float:
        """
        Calculates the z value of the plane
        :param x:
        :param y:
        :return:
        """
        return (-self.a * x - self.b * y - self.d) / self.c

    def point_distance(self, point: Point) -> float:
        """
        Calculates the distance between a point and the plane
        :param point:
        :return: Distance between point and the plane
        """
        if point is None:
            raise ValueError("point cannot be None")

        return point_plane_dist(point, self)

    @property
    def distances(self) -> np.array:
        """
        Calculates all distances between the points and the plane
        :return:
        """
        df = pcd_to_df(self.pcd)
        X, Y, Z = df["X"], df["Y"], df["Z"]

        distances = np.zeros(len(X))
        for i in range(len(X)):
            x = X[i]
            y = Y[i]
            z = Z[i]

            distances[i] = self.point_distance(Point(x, y, z))

        return distances

    @property
    def mean_dist(self) -> float:
        """
        Calculates the mean distance between the points and the plane
        :return:
        """
        return np.mean(self.distances)

    @property
    def dist_std(self) -> float:
        """
        Calculates the standard deviation of the distances between the points and the plane
        :return:
        """
        return np.std(self.distances)

    @property
    def normal_vector(self) -> np.array:
        """
        Calculates the normal vector of the plane
        :return:
        """
        return np.array([self.a, self.b, self.c])

    @property
    def norm_vec_devs(self) -> np.array:
        """
        Calculates the deviation between and the estimated normal vectors of the segmented point cloud
        :return: Numpy array with the angles between the normal vectors given in degrees
        """
        # TODO: Test
        pcd = self.pcd
        pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(
            radius=Config.SEARCH_RADIUS.value,
            max_nn=Config.MAX_NEAREST_NEIGHBOURS.value
        ))

        normals = np.asarray(pcd.normals)
        deviation = np.zeros(len(normals))

        for i, normal in enumerate(normals):
            deviation[i] = vector_angle(v1=self.normal_vector, v2=normal)

        return deviation

    @property
    def mean_angle_dev(self) -> float:
        """
        Calculates the mean deviation between the estimated normal vectors of the plane and a normal vector of the plane
        :return: Mean deviation
        """
        return np.mean(self.norm_vec_devs)
