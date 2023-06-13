from __future__ import annotations

from typing import TYPE_CHECKING

import numpy as np

if TYPE_CHECKING:
    from ..modules import Plane, Point


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


def rad_to_deg(rad: float) -> float:
    """
    Converts radians to degrees
    :param rad: Radians
    :return:
    """
    if rad is None:
        raise ValueError("Radians cannot be None")

    return np.rad2deg(rad)


def deg_to_rad(deg: float) -> float:
    """
    Converts degrees to radians
    :param deg: Degrees
    :return:
    """
    if deg is None:
        raise ValueError("Degrees cannot be None")

    return np.deg2rad(deg)


def vector_angle(v1: np.array, v2: np.array) -> float:
    """
    Calculates the angle between two vectors
    :param v1: Vector 1
    :param v2: Vector 2
    :return: Angle in degrees
    """
    return rad_to_deg(np.arccos(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))))
