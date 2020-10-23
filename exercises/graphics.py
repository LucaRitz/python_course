import abc
from math import pi


class Position:

    def __init__(self, x, y):
        self.x = x
        self.y = y


class Shape(metaclass=abc.ABCMeta):

    def __init__(self, position):
        self._position = position

    @classmethod
    def __subclasshook__(cls, subclass):
        return (hasattr(subclass, 'area') and
                callable(subclass.area) and
                hasattr(subclass, 'move') and
                callable(subclass.move) or
                NotImplemented)

    @abc.abstractmethod
    def area(self):
        return 0

    def move(self, dx, dy):
        self._position = Position(self._position.x + dx, self._position.y + dy)


class Group:

    def __init__(self, shapes):
        self.shapes = shapes

    def area(self):
        return sum(map(lambda shape: shape.area(), self.shapes))


class Ellipse(Shape):
    def __init__(self, position, radius_a, radius_b):
        super().__init__(position)
        self.__radius_a = radius_a
        self.__radius_b = radius_b

    def area(self):
        return self.__radius_a * self.__radius_b * pi


class Circle(Ellipse):

    def __init__(self, position, radius):
        super().__init__(position, radius, radius)


class Rectangle(Shape):

    def __init__(self, position, width, height):
        super().__init__(position)
        self.__width = width
        self.__height = height

    def area(self):
        return self.__width * self.__height


class Square(Rectangle):

    def __init__(self, position, size):
        super().__init__(position, size, size)
