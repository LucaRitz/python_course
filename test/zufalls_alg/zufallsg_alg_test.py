import unittest
import zufallsg_alg.freiwalds as freiwalds


class IsEqualTest(unittest.TestCase):

    def test_is_equal_getTrue(self):
        a = [
            [5, 10,  4,  2],
            [2,  7,  9,  4],
            [10, 2,  3,  1],
            [7,  9,  0,  2]
        ]

        b = [
            [3,  7,  2,  3],
            [7,  9,  9,  1],
            [11, 2,  3,  8],
            [1,  3,  4,  4]
        ]

        c = [
            [131, 139, 120,  65],
            [158, 107, 110, 101],
            [78,   97,  51,  60],
            [86,  136, 103,  38]]

        # Act
        result = freiwalds.is_equal(a, b, c, 5)

        # Assert
        self.assertTrue(result)

    def test_is_equal_getFalse(self):
        a = [
            [4, 10,  4,  2],
            [2,  7,  9,  4],
            [10, 2,  3,  1],
            [7,  9,  0,  2]
        ]

        b = [
            [3,  7,  2,  3],
            [7,  9,  9,  1],
            [11, 2,  3,  8],
            [1,  3,  4,  4]
        ]

        c = [
            [131, 139, 120,  65],
            [158, 107, 110, 101],
            [78,   97,  51,  60],
            [86,  136, 103,  38]]

        # Act
        result = freiwalds.is_equal(a, b, c, 5)

        # Assert
        self.assertFalse(result)
