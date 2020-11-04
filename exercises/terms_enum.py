import math
import sys

# to be able to specify type annotations and static type checker mypy
from typing import List, Any, Set, Dict, Tuple, Optional
# importation of abc module for abstract base classes
from abc import ABCMeta, abstractmethod
# for enum support
from enum import Enum, unique


class ContextError(Exception):

    def __init__(self, message) -> None:
        self.message = message


class Context:
    """
    Stores the values assigned to the variables into a lookup table (a dictionary).
    Each entry of the lookup table is a pair (name of variable, value)
    Some methods allows us to bind a value to a named variable,
    to change the assignement and to evaluate a variable.
    """
    def __init__(self) -> None:
        "Just create an empty dictionary"
        self.lookup_table : Dict[str, float] = {}

    def bind(self, name: str, value: float) -> None:
        """
        If the variable, called name, does not exists in the dictionary 
        lookup_table then a new assigment is added into the dictionary otherwise
        the value of the variable is changed.
        :param name: name of the variable
        :param value: value to assign to the variable
        """
        if not name: # is name empty
            raise ContextError("The variable's name is empty")
        self.lookup_table[name] = value  # create entry and/or change value

    def get_value(self, name: str) -> float:
        if not name: # name is empty
            raise ContextError("The variable's name is empty")
        if name in self.lookup_table:
            return self.lookup_table[name]
        else:
            raise ContextError("The variable '" + name + "' is not bound to a value")

@unique
class Bin_op(Enum):
    """Enumeration of all supported binary operators"""
    ADD = 1
    SUB = 2
    MUL = 3
    DIV = 4
    
    
@unique
class Una_op(Enum):
    """Enumeration of all supported unary operators"""
    NEG = 1
    
class Term(metaclass=ABCMeta):
    """
    This abstract class defines a abstract method that evaluates
    a term (expression)
    """
    @abstractmethod
    def eval(self, context: Context) -> float:
        """
        Abstract method that evaluate a term.
        :param context: where the bindings (variable name, value) are stored
        :return: the value of the evaluated term
        """
        pass               # no implementation
           
class Constant(Term):
    """
    The value of a constant cannot (obviously) change.
    The value is initialized during the creation.
    """
    def __init__(self, value :float) -> None:
        """
        Defines the constant value.
        :param value: the constant value to initialize
        """
        self.value = value 

    def eval(self, context: Context) -> float:
        """
        :return: simply the value 
        """
        return self.value

    
class Variable(Term):
    """
    The value of a variable can be modified via the context object.
    """
    def __init__(self, name: str) -> None:
        """
        A variable is created and added to the context
        :param context: dictionnary of bindings, this object is not stored as an attribute
        :param name: name of the variable
        :param value: value of the variable
        """
        self.name = name

    def eval(self, context: Context ) -> float:
        """
        :return: the value of the variable
        """
        return context.get_value(self.name)

   
class Binary_expression(Term):
    """
    A binary expression has two terms (left, right) and a binary operator.
    """
    def __init__(self, left: Term, right: Term, bin_op: Bin_op) -> None:
        """
        :param left: left term
        :param right: right term
        :param bin_op: binary operator (enum)
        """
        self.left = left
        self.right = right
        self.bin_op = bin_op

    def eval(self, context: Context) -> float:
        """
        Evaluates both the terms first and then apply the binary_operator
        :return: the evaluated value of the binary expression
        """
        value_left  = self.left.eval(context)
        value_right = self.right.eval(context)
        bin_op_dict = {Bin_op.ADD: lambda l, r : l + r,
                       Bin_op.SUB: lambda l, r : l - r,
                       Bin_op.MUL: lambda l, r : l * r,
                       Bin_op.DIV: lambda l, r : l / r
        }

        operation = bin_op_dict[self.bin_op]
        return operation(value_left, value_right)

    
class Unary_expression(Term):
    """
    A unary expression has on term and a unary operator.
    """
    def __init__(self, term: Term, una_op: Una_op) -> None:
        """
        :param term: single term
        :param una_op: binary operator (enum)
        """
        self.term = term
        self.una_op = una_op

    def eval(self, context: Context) -> float:
        """
        Evaluates both the terms first and then apply the binary_operator
        :return: the evaluated value of the binary expression
        """
        value_term  = self.term.eval(context)
        una_op_dict = {Una_op.NEG: lambda t : (-1) * t }
        operation = una_op_dict[self.una_op]
        return operation(value_term)

    
def main() -> None:
    """ Launcher """
    ctx = Context()
    three = Constant(3)
    five  = Constant(5)
    print("Constant 3: ", three.eval(ctx))
    print("Constant 5: ", five.eval(ctx))
    v = Variable("d") 
    ctx.bind("d", 7)      # define d = 7
    print("Variable d: ", v.eval(ctx))
    neg = Unary_expression(v, Una_op.NEG)
    print("-d: ", neg.eval(ctx))
    addition = Binary_expression(three, neg, Bin_op.ADD)
    print("3 + -d: ", addition.eval(ctx))
    multiplication = Binary_expression(addition, five, Bin_op.MUL)
    print("(3 + -d) * 5: ", multiplication.eval(ctx))

    
if __name__ == "__main__":
    main()
