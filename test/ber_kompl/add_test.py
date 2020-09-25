import unittest
from parameterized import parameterized
import ber_kompl.add as add


class IsEqualTest(unittest.TestCase):

    @parameterized.expand([
        [['0', '0', '1', '0', '0', '0', '0'], True, 6],
        [['0', '0', '1', '0', '0', '0', '0', '1'], False, 6],
        [['0', '0', '1', '0', '0', '0', '0', '1', '0'], False, 7],
    ])
    def test_getExpected(self, input_value, accepted, result):
        machine, output_tape = add.build()

        # Act
        machine.input_value(input_value)

        # Assert
        self.assertEqual(accepted, machine.accepted())
        if accepted:
            self.assertEqual(result, self.count(output_tape))

    @staticmethod
    def count(output_tape):
        print(output_tape.get_value())
        return len(output_tape.get_value()) - 1
