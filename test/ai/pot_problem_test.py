import unittest

from parameterized import parameterized

import ai.pot_problem as problem


class PotProblemTest(unittest.TestCase):

    @parameterized.expand([
        [problem.ai.bfs],
        [problem.ai.ucs],
        [problem.ai.dfs],
        [problem.ai.dls, [5]],
        [problem.ai.ids, [5]]
    ])
    def test_searchFunctions(self, strategy, additional_params=None):
        initial_state = [(12, 0), (8, 0), (3, 0)]

        # Act
        result = problem.ai.graph_search(problem.expand_pot, problem.goal_test, strategy,
                                         [problem.ai.SearchNode(initial_state, 0, 0, None)], additional_params)

        # Assert
        self.assertIsNotNone(result)
        print(result.p)
        print(result.state)
