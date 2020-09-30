import ai.model as ai
from enum import Enum


class Position(Enum):
    left = 0
    right = 1

    @staticmethod
    def invert(position):
        return Position.left if position == Position.right else Position.right


class Person:

    def __init__(self, speed):
        self.speed = speed

    def __eq__(self, other):
        if not isinstance(other, Person):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.speed == other.speed


class Action:

    def __init__(self, person, companion, position):
        self.person = person
        self.companion = companion
        self.position = position

    def __eq__(self, other):
        if not isinstance(other, Action):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return (self.person == other.person and
                self.companion == other.companion and
                self.position == other.position)


class BridgeAndTorchSearchNode(ai.SearchNode):

    def __init__(self, state, d=0, p=0, a=None, visited_states=[]):
        super().__init__(state, d, p, a)
        self.visited_states = visited_states

    @classmethod
    def from_copy(cls, node, visited_states):
        return cls(node.state, node.d, node.p, node.a, visited_states)

    def expand(self):
        expanded = []

        torch_position = self.state[-1][1]
        state_without_torch = self.state[:-1]

        for person_index, person in enumerate(state_without_torch):
            if torch_position == person[1]:
                for companion_index, companion in enumerate(state_without_torch):
                    if person[1] == companion[1]:
                        new_pos = Position.invert(person[1])
                        action = Action(person, companion, new_pos)
                        acc_cost = self.p + max(person[0].speed, companion[0].speed)
                        new_state = state_without_torch.copy()
                        new_state.remove(person)
                        new_state.insert(person_index, tuple((person[0], new_pos)))
                        if person[0] != companion[0]:
                            new_state.remove(companion)
                            new_state.insert(companion_index, tuple((companion[0], new_pos)))
                        new_state.append(tuple((None, new_pos)))

                        if new_state not in self.visited_states or BridgeAndTorchSearchNode.test_goal(new_state):
                            self.visited_states.append(new_state)
                            expanded.append(BridgeAndTorchSearchNode(new_state, self.d + 1, acc_cost, action))
        return list(map(lambda node: BridgeAndTorchSearchNode.from_copy(node, self.visited_states), expanded))

    def is_goal(self):
        return BridgeAndTorchSearchNode.test_goal(self.state)

    @staticmethod
    def test_goal(state):
        goals = list(filter(lambda person: person[1] == Position.right, state))
        return len(goals) == len(state)


def find_solution(persons):
    start_state = list(map(lambda person: tuple((person, Position.left)), persons)) + [tuple((None, Position.left))]
    start_node = BridgeAndTorchSearchNode(start_state)
    return ai.search(start_node, ai.BestFirstStrategy())
