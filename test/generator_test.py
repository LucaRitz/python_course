import exercises.generator as gen
import unittest


class FibonacciGeneratorTest(unittest.TestCase):

    def test_generator_fibonacci(self):
        expected_results = (1, 1, 2, 3, 5, 8, 13, 21, 34)

        # Act
        fib_generator = gen.generator_fibonacci()

        # Assert
        for expected in expected_results:
            result = next(fib_generator)
            self.assertEqual(expected, result)
