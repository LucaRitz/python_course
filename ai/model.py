
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
