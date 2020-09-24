import random


def is_equal(a, b, c, k):
    for i in range(k):
        r = random_binary_vector(len(a))
        x = multiply_matrix(b, [r])
        y = multiply_matrix(a, x)
        z = multiply_matrix(c, [r])
        if not are_vectors_equal(z, y):
            return False

    return True


def are_vectors_equal(a, b):
    for i in range(len(a)):
        if a[i] != b[i]:
            return False
    return True


def multiply_matrix(a, b):
    result = [[0 for i in range(len(a))] for j in range(len(a))]

    for i in range(len(a)):
        for j in range(len(b)):
            for k in range(len(a)):
                result[i][k] += a[i][j] * b[j][k]
    return result


def random_binary_vector(size):
    vector = []
    for i in range(size):
        vector.append(random.randint(0, 1))
    return vector
