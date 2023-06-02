from dataclasses import dataclass

import numpy as np

from src.logging.logger import Logger


@dataclass
class Plane:
    __a: float  # x
    __b: float  # y
    __c: float  # z
    __d: float  # Distance from origin
    __inliers_indexes: list  # Inliers

    def __init__(self, a: float, b: float, c: float, d: float, inliers_indexes: np.array) -> None:
        """
        Constructor for the Plane class
        :param a:
        :param b:
        :param c:
        :param d:
        """
        self.__a = a
        self.__b = b
        self.__c = c
        self.__d = d
        self.__inliers_indexes = inliers_indexes
        Logger.log(__file__).info(f"Plane created with {len(self.__inliers_indexes)} inliers")

    @property
    def a(self) -> float:
        """
        Getter for a
        :return:
        """
        return self.__a

    @property
    def b(self) -> float:
        """
        Getter for b
        :return:
        """
        return self.__b

    @property
    def c(self) -> float:
        """
        Getter for c
        :return:
        """
        return self.__c

    @property
    def d(self) -> float:
        """
        Getter for d
        :return:
        """
        return self.__d

    @property
    def inlier_indexes(self) -> list:
        """
        Getter for inlier indexes
        :return:
        """
        return self.__inliers_indexes

    def z(self, x: float, y: float) -> float:
        """
        Calculates the z value of the plane
        :param x:
        :param y:
        :return:
        """
        return (-self.a * x - self.b * y - self.d) / self.c

    def z_distance(self, pcd_z: float) -> float:
        """
        Calculates
        :return:
        """
        pass
