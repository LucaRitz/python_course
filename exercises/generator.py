

def generator_fibonacci():
    prev_1: int = 1
    prev_2: int = 1
    index: int = 0
    while True:
        if index <= 1:  # Base-Case
            yield 1
        else:
            current: int = prev_1 + prev_2
            prev_2 = prev_1
            prev_1 = current
            yield current
        index += 1
