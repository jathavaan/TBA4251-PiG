from dataclasses import dataclass

import open3d as o3d

from src.logging.logger import Logger
from src.modules.point import Point
from src.utils.computation_utils import point_plane_dist


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

        Logger.log(__file__).debug(f"Plane created with {len(self.__pcd.points)} inliers")

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
            Logger.log(__file__).warning("Point cloud has no points")

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
