import unittest
import random
from parameterized import parameterized
import exercises.basics as basics


class IsEvenTest(unittest.TestCase):

    def test_isNotEven_getFalse(self):
        # Act
        result = basics.is_even(random.randrange(2, 10, 2) - 1)

        # Assert
        self.assertFalse(result)

    def test_isEven_getTrue(self):
        # Act
        result = basics.is_even(random.randrange(0, 10, 2))

        # Assert
        self.assertTrue(result)


class ComputeAreaTest(unittest.TestCase):

    @parameterized.expand([
        [10, 314.1592653589],
        [2, 12.566370614359],
    ])
    def test_compute_area_getExpected(self, radius, expected):
        # Act
        result = basics.compute_area(radius)

        # Assert
        self.assertAlmostEqual(expected, result)


class GreatestValueTest(unittest.TestCase):
    @parameterized.expand([
        [[2, 10, 100, 20], 100],
        [[10, 5, 1], 10],
        [[], 0]
    ])
    def test_greatest_value_getExpected(self, values, expected):
        # Act
        result = basics.greatest_value(values)

        # Assert
        self.assertEqual(expected, result)


class ReverseTest(unittest.TestCase):
    @parameterized.expand([
        [[], []],
        [[1, 10, 5, 7, 2], [2, 7, 5, 10, 1]]
    ])
    def test_reverse_getExpected(self, values, expected):
        # Act
        result = basics.reverse(values)

        # Assert
        self.assertEqual(expected, result)


class InsertAscTest(unittest.TestCase):
    @parameterized.expand([
        [[], 1, [1]],
        [[1,2], 1, [1, 1, 2]],
        [[1,2,3], 4, [1,2,3,4]],
        [[1,2,1], 2, [1,2,2,1]],
        [[1,2,3,2], 3, [1,2,3,3,2]]
    ])
    def test_insert_asc_getExpected(self, values, to_insert, expected):
        # Act
        result = basics.insert_asc(values, to_insert)

        # Assert
        self.assertEqual(expected, result)


class InsertionSortTest(unittest.TestCase):
    @parameterized.expand([
        [[], []],
        [[1, 2], [1, 2]],
        [[3, 2, 1], [1, 2, 3]],
        [[9, 7, 3, 8, 2, 9], [2, 3, 7, 8, 9, 9]]
    ])
    def test_insertion_sort_getExpected(self, values, expected):
        # Act
        result = basics.insertion_sort(values)

        # Assert
        self.assertEqual(expected, result)


class LstLenTest(unittest.TestCase):
    @parameterized.expand([
        [[], []],
        [['hallo'], [5]],
        [['ab', 'test'], [2, 4]],
        [['abc', 'de', 'fghi'], [3, 2, 4]]
    ])
    def test_lst_len_getExpected(self, values, expected):
        # Act
        result = basics.lst_len(values)

        # Assert
        self.assertEqual(expected, result)


if __name__ == '__main__':
    unittest.main()
