import random

class SearchNode:

    def __init__(self, state, d, p, a):
        self.state = state
        self.d = d
        self.p = p
        self.a = a

    def expand(self):
        pass

    def is_goal(self):
        pass

    def __eq__(self, other):
        if not isinstance(other, SearchNode):
            # don't attempt to compare against unrelated types
            return NotImplemented

        return self.state == other.state


class Strategy:

    def get_candidate(self, candidates):
        pass


class BestFirstStrategy(Strategy):

    def get_candidate(self, candidates):
        best_candidate = None
        for candidate in candidates:
            best_candidate = best_candidate if best_candidate is not None and best_candidate.p <= candidate.p else candidate
        return best_candidate


def search(start_node, strategy):
    candidates = [start_node]
    return __search_with_candidates(candidates, strategy)


def __search_with_candidates(candidates, strategy):
    while candidates:
        candidate = strategy.get_candidate(candidates)
        if candidate.is_goal():
            return candidate
        candidates.remove(candidate)
        candidates += candidate.expand()
    return None

#########################################################################


def graph_search(expand, goal_test, strategy, fringe, args=None):
    closed = []
    while fringe:
        node = strategy(fringe) if args is None else strategy(fringe, *args)
        fringe.remove(node)

        if goal_test(node):
            return node
        if node not in closed:
            closed.append(node)
            fringe.extend(expand(node))
    return None


def bfs(candidates):
    result = None
    for candidate in candidates:
        result = result if result is not None and result.d <= candidate.d else candidate
    return result


def ucs(candidates):
    result = None
    for candidate in candidates:
        result = result if result is not None and result.p <= candidate.p else candidate
    return result


def dfs(candidates):
    return dls(candidates, None)


def dls(candidates, l=None):
    result = None
    for candidate in candidates:
        if l is not None and candidate.d > l:
            continue
        result = result if result is not None and result.d >= candidate.d else candidate
    return result


def ids(candidates, limit):
    result = None
    for l in range(limit):
        result = dls(candidates, l)
        if result is not None:
            break
    return result


######################################################
def genetic_algorithm(population, reproduce_fnc, mutate_fnc, fitness_fnc, max_epoch):
    for current_epoch in range(max_epoch):
        new_population = []
        for i in range(len(population)):
            x = __random_select(population, fitness_fnc)
            y = __random_select(population, fitness_fnc)
            child = reproduce_fnc(x, y)
            if __do_mutate():
                child = mutate_fnc(child)
            new_population.extend(child)
        population = new_population
    return __best(population, fitness_fnc)


def __random_select(population, fitness_fnc):
    range_of_parent = {}
    counter = 0
    for parent in population:
        fitness = fitness_fnc(parent)
        range_of_parent[(counter, counter + fitness)] = parent
        counter += fitness + 1

    ticket = random.randrange(0, counter - 1)
    for tickets in range_of_parent:
        if tickets[0] <= ticket <= tickets[1]:
            return range_of_parent[tickets]
    return None


def __do_mutate():
    number = random.randrange(0, 1000)
    return number == 1


def __best(population, fitness_fnc):
    best = None
    best_fitness = 0

    for pop in population:
        fitness = fitness_fnc(pop)
        if fitness > best_fitness:
            best = pop
            best_fitness = fitness

    return best
