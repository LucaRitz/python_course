import exercises.graphics as graphic
import unittest
from math import pi


class EllipseTest(unittest.TestCase):

    def test_area_right(self):
        radius_a = 2
        radius_b = 6
        ellipse = graphic.Ellipse(graphic.Position(0, 0), radius_a, radius_b)

        # Act
        result = ellipse.area()

        # Assert
        self.assertEqual(radius_a * radius_b * pi, result)


class CircleTest(unittest.TestCase):

    def test_area_right(self):
        radius = 2
        circle = graphic.Circle(graphic.Position(0, 0), radius)

        # Act
        result = circle.area()

        # Assert
        self.assertEqual(radius ** 2 * pi, result)


class RectangleTest(unittest.TestCase):

    def test_area_right(self):
        width = 10
        height = 5

        rectangle = graphic.Rectangle(graphic.Position(0, 0), width, height)

        # Act
        result = rectangle.area()

        # Assert
        self.assertEqual(width * height, result)


class SquareTest(unittest.TestCase):

    def test_area_right(self):
        size = 4

        square = graphic.Square(graphic.Position(0, 0), size)

        # Act
        result = square.area()

        # Assert
        self.assertEqual(size ** 2, result)


class GroupTest(unittest.TestCase):

    def test_area_right(self):
        radius_a = 2
        radius_b = 6
        size = 10

        ellipse = graphic.Ellipse(graphic.Position(0, 0), radius_a, radius_b)
        square = graphic.Square(graphic.Position(0, 0), 10)
        group = graphic.Group((ellipse, square))

        # Act
        result = group.area()

        # Assert
        self.assertEqual(radius_a * radius_b * pi + size ** 2, result)
