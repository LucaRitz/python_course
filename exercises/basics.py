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


def flat(value):
    flattened = []
    while value:
        flattened.extend(value.pop(0))
    return flattened


def remove_min_max(dict):
    min_key = None
    min_value = None
    max_key = None
    max_value = None

    result = dict.copy()

    for key, value in dict.items():
        min_value = value if min_value is None else min(min_value, value)
        if min_value == value:
            min_key = key

        max_value = value if max_value is None else max(max_value, value)
        if max_value == value:
            max_key = key

    del result[max_key]
    del result[min_key]
    return result


class PhoneKeyboard:

    def __init__(self):
        self.digits = ''

    def press(self, digit):
        if len(self.digits) < 10 and len(digit) == 1 and digit in '0123456789':
            self.digits += digit

    def dial(self):
        result = ''
        if len(self.digits) == 10:
            print('dial: ' + self.digits)
            result = self.digits
            self.clear()
        else:
            print('Not enough numbers')
        return result

    def clear(self):
        self.digits = ''

    def backspace(self):
        self.digits = self.digits[:-1]


class Car:

    def __init__(self, gas_consumption):
        self.gas_consumption = gas_consumption
        self.tank_size = 30
        self.tank_fill = 0

    def fill(self, liters):
        space_in_tank = self.tank_size - self.tank_fill
        self.tank_fill += min(space_in_tank, liters)

    def drive(self, km):
        used_liters = (km * self.gas_consumption) / 100
        self.tank_fill -= min(self.tank_fill, used_liters)

    def gas(self):
        return self.tank_fill
