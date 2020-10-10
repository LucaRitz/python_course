import unittest

import ai.eight_dame as ed


class EightDameTest(unittest.TestCase):

    def test_eightDame(self):
        # Act
        result = ed.eight_dame(1_000_000)

        # Assert
        self.assertIsNotNone(result)
        print(ed.fitness_fnc(result))
        print_result(result)


def print_result(result):
    for inx in range(0, 8):
        for pos in result:
            if pos - 1 == inx:
                print('|X|', end='')
            else:
                print('|-|', end='')
        print('')
    print('', flush=True)
