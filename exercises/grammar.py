import math
import abc


class Term(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def eval(self, context):
        return 0.0


@Term.register
class Constant:

    def __init__(self, value):
        self.__value = value

    def eval(self, context):
        return self.__value


@Term.register
class Variable:

    def __init__(self, name):
        self.__name = name

    def eval(self, context):
        return context.get_value(self.__name)


@Term.register
class BinaryExpression:

    def __init__(self, binary_operator, left, right):
        self.__binary_operator = binary_operator
        self.__left = left
        self.__right = right

    def eval(self, context):
        value_left = self.__left.eval(context)
        value_right = self.__right.eval(context)
        if '+' == self.__binary_operator:
            return value_left + value_right
        if '-' == self.__binary_operator:
            return value_left - value_right
        if '*' == self.__binary_operator:
            return value_left * value_right
        if '/' == self.__binary_operator:
            return value_left / value_right


@Term.register
class UnaryExpression:

    def __init__(self, unary_operator, term):
        self.__unary_operator = unary_operator
        self.__term = term

    def eval(self, context):
        value = self.__term.eval(context)
        if '-' == self.__unary_operator:
            return -value
        return value

class Context:

    def __init__(self):
        self.lookup_table = {}

    def bind(self, name, value):
        self.lookup_table[name] = value

    def get_value(self, name):
        if name in self.lookup_table.keys():
            return self.lookup_table[name]
        return 0
