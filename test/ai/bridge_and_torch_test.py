import unittest
import ai.bridge_and_torch as bat


class BridgeAndTorchTest(unittest.TestCase):

    def test_IsBestSolutionLowerOrEqualsThan15(self):
        persons = [bat.Person(1), bat.Person(2), bat.Person(5), bat.Person(8)]

        # Act
        result = bat.find_solution(persons)

        # Assert
        self.assertIsNotNone(result)
        self.assertTrue(result.p <= 15)
        print(result.p)
