import unittest
import exercises.terms_enum as term
import random


class TermTest(unittest.TestCase):

    def test_term(self):
        ctx = term.Context()
        three = term.Constant(3)
        five = term.Constant(5)
        print("Constant 3: ", three.eval(ctx))
        print("Constant 5: ", five.eval(ctx))
        v = term.Variable("d")
        ctx.bind("d", 7)  # define d = 7
        print("Variable d: ", v.eval(ctx))
        neg = term.Unary_expression(v, term.Una_op.NEG)
        print("-d: ", neg.eval(ctx))
        addition = term.Binary_expression(three, neg, term.Bin_op.ADD)
        print("3 + -d: ", addition.eval(ctx))
        multiplication = term.Binary_expression(addition, five, term.Bin_op.MUL)
        print("(3 + -d) * 5: ", multiplication.eval(ctx))

        # Act
        result: float = multiplication.eval(ctx)

        # Assert
        self.assertEqual(-20, result)


class ContextTest(unittest.TestCase):

    def test_bind_emptyName_raiseException(self):
        context: term.Context = term.Context()

        # Act
        self.assertRaises(term.ContextError, context.bind, '', random.random())

    def test_bind_noEmptyName_doNotRaiseException(self):
        context: term.Context = term.Context()

        # Act
        context.bind('val', random.random())

    def test_getValue_emptyName_raiseException(self):
        context: term.Context = term.Context()

        # Act
        self.assertRaises(term.ContextError, context.get_value, '')

    def test_getValue_noKeyPresent_raiseException(self):
        context: term.Context = term.Context()

        # Act
        self.assertRaises(term.ContextError, context.get_value, 'not_present')

    def test_getValue_hasKey_getExpected(self):
        key: str = str(random.random())
        expected_value: float = random.random()

        context: term.Context = term.Context()
        context.bind(key, expected_value)

        # Act
        result: float = context.get_value(key)

        # Assert
        self.assertEqual(expected_value, result)
