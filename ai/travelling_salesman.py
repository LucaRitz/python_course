import random


def traveller(node, max_epoch):
    roundtrip = generate_random_roundtrip(node)
    for trip in roundtrip:
        print(trip.id)
    return roundtrip



def generate_random_roundtrip(start_node):
    roundtrip = [start_node]
    __expand_node(start_node, roundtrip)
    roundtrip = __close_cycle(roundtrip)

    return roundtrip


def __expand_node(node, roundtrip):
    unvisited_nodes = node.children.copy()
    while unvisited_nodes:
        to_visit = __pop_random(unvisited_nodes)[0]
        if to_visit not in roundtrip:
            roundtrip.append(to_visit)
            __expand_node(to_visit, roundtrip)


def __close_cycle(roundtrip):
    first_node = roundtrip[0]
    last_node = roundtrip[-1]
    returnToStart = __greedy_shortest_path(last_node, first_node, [])
    return roundtrip + returnToStart[1:-2]


def __greedy_shortest_path(start, end, expanded, cost=0):
    if start == end:
        return [start]
    else:
        children_with_acc_cost = list(map(lambda child: (child[0], child[1] + cost), start.children))
        expanded.extend(children_with_acc_cost)
        next_child = __find_closest(expanded)

        if next_child is not None:
            path_of_children = __greedy_shortest_path(next_child[0], end, expanded, next_child[1])
            if path_of_children:
                return [start] + path_of_children

    return []


def __find_closest(expanded):
    next_child = None
    for child in expanded:
        if next_child is None or child[1] < next_child[1]:
            next_child = child
    expanded.remove(next_child)

    return next_child


def __pop_random(nodes):
    return nodes.pop(random.randrange(0, len(nodes)))


class Node:

    def __init__(self, id):
        self.id = id
        self.children = []

    def append_child(self, child, distance):
        self.children.append((child, distance))

    def measure_distance(self, nodes):
        pass

    # def __eq__(self, other):
    #    return (isinstance(other, type(self)) and
    #            self.children == other.children)
