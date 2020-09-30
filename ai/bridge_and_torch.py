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

    def __init__(self, state, d, p, a):
        super().__init__(state, d, p, a)

    def expand(self):
        expanded = []

        for person_index, person in enumerate(self.state):
            for companion_index, companion in enumerate(self.state):
                if person[1] == companion[1]:
                    new_pos = Position.invert(person[1])
                    action = Action(person, companion, new_pos)
                    acc_cost = self.p + max(person[0].speed, companion[0].speed)
                    new_state = self.state.copy()
                    new_state.remove(person)
                    new_state.insert(person_index, tuple((person[0], new_pos)))
                    if person[0] != companion[0]:
                        new_state.remove(companion)
                        new_state.insert(companion_index, tuple((companion[0], new_pos)))
                    expanded.append(BridgeAndTorchSearchNode(new_state, self.d + 1, acc_cost, action))
        return expanded

    def is_goal(self):
        goals = list(filter(lambda person: person[1] == Position.right, self.state))
        return len(goals) == len(self.state)


def find_solution(persons):
    start_state = list(map(lambda person: tuple((person, Position.left)), persons))
    start_node = BridgeAndTorchSearchNode(start_state, 0, 0, None)
    return ai.search(start_node, ai.BestFirstStrategy())
