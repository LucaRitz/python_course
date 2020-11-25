import unittest
from exercises.append import *


class AppendTest(unittest.TestCase):

    def test_appendFiles_filesAppended(self):
        target = 'resources/result.txt'

        # Act
        append('resources/test_a.txt', 'resources/test_b.txt', target)

        # Assert
        result = read(target)
        print(result)
        self.assertTrue(result)