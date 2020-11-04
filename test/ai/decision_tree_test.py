import unittest
import ai.decision_tree as dt


class Play(unittest.TestCase):

    def test_play(self):
        # Act
        node: dt.RootNode = dt.build_decision_tree('resources/play.arff')

        dt.print_node(node)
