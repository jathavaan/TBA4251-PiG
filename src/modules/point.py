from dataclasses import dataclass


@dataclass
class Point:
    __x: float
    __y: float
    __z: float

    def __init__(self, x: float, y: float, z: float) -> None:
        """
        Constructor for the Point class
        :param x:
        :param y:
        :param z:
        """
        self.x = x
        self.y = y
        self.z = z

    @property
    def x(self) -> float:
        """
        Getter for x
        :return:
        """
        return self.__x

    @x.setter
    def x(self, x: float) -> None:
        """
        Setter for x
        :param x:
        :return:
        """
        if x is None:
            raise ValueError("x cannot be None")

        self.__x = x

    @property
    def y(self) -> float:
        """
        Getter for y
        :return:
        """
        return self.__y

    @y.setter
    def y(self, y: float) -> None:
        """
        Setter for y
        :param y:
        :return:
        """
        if y is None:
            raise ValueError("y cannot be None")

        self.__y = y

    @property
    def z(self) -> float:
        """
        Getter for z
        :return:
        """
        return self.__z

    @z.setter
    def z(self, z: float) -> None:
        """
        Setter for z
        :param z:
        :return:
        """
        if z is None:
            raise ValueError("z cannot be None")

        self.__z = z

    def __eq__(self, other):
        """
        Override for the equality operator
        :param other:
        :return:
        """
        if not isinstance(other, Point):
            return False

        return self.x == other.x and self.y == other.y and self.z == other.z