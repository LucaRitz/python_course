import math


def is_even(value):
    return value % 2 == 0


def compute_area(radius):
    return math.pi * radius ** 2


def greatest_value(values):
    result = 0
    for value in values:
        result = max(result, value)
    return result


def reverse(values):
    return values[::-1]


def insert_asc(list, to_insert):
    result = []
    was_inserted = False

    for value in list:
        if value >= to_insert and not was_inserted:
            result.append(to_insert)
            was_inserted = True
        result.append(value)

    if not was_inserted:
        result.append(to_insert)

    return result


def insertion_sort(list):
    result = []
    for value in list:
        result = insert_asc(result, value)
    return result


def lst_len(strings):
    result = []
    for value in strings:
        length = 0
        for _ in value:
            length += 1
        result.append(length)
    return result
