import numpy as np

from src.modules.plane import Plane
from src.modules.point import Point


def point_plane_dist(point: Point, plane: Plane) -> float:
    """
    Calculates the distance between a point and a plane
    :param point: Point object
    :param plane: Plane object
    :return:
    """
    return abs(
        plane.a * point.x + plane.b * point.y + plane.c * point.z + plane.d
    ) / np.sqrt(
        plane.a ** 2 + plane.b ** 2 + plane.c ** 2
    )


def std(data: np.ndarray) -> float:
    """
    Calculates the standard deviation of a numpy array
    :param data: Numpy array
    :return:
    """
    return np.std(data)
