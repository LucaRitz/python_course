import ai.model as ai


def expand_pot(node):
    candidates = []

    for source_inx, source_pot in enumerate(node.state):
        for target_inx, target_pot in enumerate(node.state):

            new_state = node.state.copy()

            # Empty pot
            if source_pot == target_pot:
                if source_pot[1] > 0:
                    new_state[source_inx] = (source_pot[0], 0)
                    candidates.append(ai.SearchNode(new_state, node.d + 1, node.p + 1, None))
                continue

            # Pour over from pot to pot
            if source_pot[1] > 0 and target_pot[0] > target_pot[1]:
                space_in_target = target_pot[0] - target_pot[1]
                poured_over = min(space_in_target, source_pot[1])
                new_state[source_inx] = (source_pot[0], source_pot[1] - poured_over)
                new_state[target_inx] = (target_pot[0], poured_over)
                candidates.append(ai.SearchNode(new_state, node.d + 1, node.p + 1, None))

        # Fill pot
        if source_pot[1] < source_pot[0]:
            new_state = node.state.copy()
            new_state[source_inx] = (source_pot[0], source_pot[0])
            candidates.append(ai.SearchNode(new_state, node.d + 1, node.p + 1, None))
    return candidates


def goal_test(node):
    for state in node.state:
        if state[1] == 1:
            return True
    return False
