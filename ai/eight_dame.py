import ai.model as ai
import random


def eight_dame(max_epoch):
    population = ((1, 2, 3, 4, 5, 6, 7, 8),
                  (2, 1, 3, 4, 5, 6, 7, 8),
                  (3, 1, 2, 4, 5, 6, 7, 8),
                  (4, 1, 2, 3, 4, 5, 6, 7),
                  (5, 6, 7, 8, 1, 2, 3, 4),
                  (6, 5, 3, 4, 5, 6, 7, 8),
                  (5, 6, 7, 8, 9, 2, 3, 4))
    return ai.genetic_algorithm(population, __reproduce_fnc, __mutate_fnc, fitness_fnc, max_epoch)


def fitness_fnc(value):
    valid_counter = 0
    for inx, pos in enumerate(value):
        for other_inx in range(inx + 1, 8):
            other_pos = value[other_inx]
            if pos == other_pos:
                continue
            other_forbidden = abs(other_inx - inx)
            if other_pos + other_forbidden == pos or other_pos - other_forbidden == pos:
                continue
            valid_counter += 1
    return valid_counter ** 5


def __reproduce_fnc(father, mother):
    children = []
    for i in range(1):
        cut = random.randrange(0, 7)
        child = []
        for i in range(8):
            parent = father if cut <= i else mother
            child.append(parent[i])
        children.append(tuple(child))
    return children


def __mutate_fnc(children):
    new_children = []
    for child in children:
        new_child = list(child)
        mutate = random.randrange(0, 7)
        value = random.randrange(1, 8)
        new_child[mutate] = value
        new_children.append(tuple(new_child))
    return new_children
