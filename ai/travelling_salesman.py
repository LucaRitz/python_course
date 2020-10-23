import random
from dijkstar import Graph, find_path
import ai.model as ai


def traveller(node, max_epoch):
    roundtrip_1 = __generate_random_roundtrip(node)
    roundtrip_2 = __generate_random_roundtrip(node)
    roundtrip_3 = __generate_random_roundtrip(node)
    return ai.genetic_algorithm((roundtrip_1, roundtrip_2, roundtrip_3), __reproduce_fnc, lambda val: val, __get_cost, max_epoch)


def __reproduce_fnc(roundtrip_1, roundtrip_2):
    return [roundtrip_1]


def __get_cost(roundtrip):
    return 1


def __generate_random_roundtrip(start_node):
    roundtrip = [start_node]
    __expand_node(start_node, roundtrip)
    roundtrip = __close_cycle(start_node, roundtrip)

    return roundtrip


def __expand_node(node, roundtrip):
    unvisited_nodes = node.children.copy()
    while unvisited_nodes:
        to_visit = __pop_random(unvisited_nodes)[0]
        if to_visit not in roundtrip:
            roundtrip.append(to_visit)
            __expand_node(to_visit, roundtrip)


def __close_cycle(node, roundtrip):
    graph = Graph(undirected=True)
    __to_dijkstra(node, graph)
    first_node = roundtrip[0].id
    last_node = roundtrip[-1].id
    path_info = find_path(graph, last_node, first_node)

    return roundtrip + __to_nodes(node, path_info)[1:-2]


def __to_dijkstra(node, graph):
    for child in node.children:
        if node.id not in graph.get_data() or child[0].id not in graph.get_data()[node.id]:
            graph.add_edge(node.id, child[0].id, child[1])
            __to_dijkstra(child[0], graph)


def __to_nodes(node, path_info):
    path = []
    for node_id in path_info.nodes:
        path.append(__find_node(node, node_id, []))
    return path


def __find_node(node, node_id, visited):
    visited.append(node)
    if node.id == node_id:
        return node
    for child in node.children:
        if child[0] not in visited:
            return __find_node(child[0], node_id, visited)
    return None


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
