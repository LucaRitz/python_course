from enum import Enum

EMPTY = None


class Machine:

    def __init__(self, input_tape):
        self.__states = []
        self.__input_tape = input_tape
        self.__accepted = False
        self.__current_state = None
        self.__start_state = None

    def append_state(self, state):
        self.__states.append(state)

        if state.is_start_state() and self.__current_state is None:
            self.__start_state = state
            self.__current_state = state

    def accepted(self):
        return self.__accepted

    def input_value(self, value):
        self.__input_tape.value(value)
        self.update_state(self.__start_state)

    def update_state(self, next_state):
        self.__current_state = next_state if next_state is not None else self.__current_state
        if self.__input_tape.is_at_end():
            self.__accepted = self.__current_state.is_end_state()
        elif not self.__current_state.is_error_state():
            self.__current_state.work()


class State:

    def __init__(self, machine, state_type, input_tape, auxiliary_tapes, output_tape, functions):
        self.__machine = machine
        self.__state_type = state_type
        self.__input_tape = input_tape
        self.__auxiliary_tapes = auxiliary_tapes
        self.__output_tape = output_tape
        self.__functions = functions
        self.__all_input_tapes = auxiliary_tapes + [self.__input_tape]
        self.__machine.append_state(self)

    def is_end_state(self):
        return self.__state_type == StateType.end

    def is_start_state(self):
        return self.__state_type == StateType.start

    def is_error_state(self):
        return self.__state_type == StateType.error

    def work(self):
        if self.__input_tape.read() == EMPTY:
            self.__machine.update_state(self)
            return

        signs = list(map(lambda tape: tape.read(), self.__all_input_tapes))
        matching_func = list(filter(lambda func: func.matches(signs), self.__functions))

        if len(matching_func) > 0:
            next_state = matching_func[0].apply(self.__input_tape, self.__auxiliary_tapes, self.__output_tape)
            self.__machine.update_state(next_state)
        else:
            next_state = ErrorState(self.__machine)
            self.__machine.update_state(next_state)

    class Builder:
        def __init__(self, state_type, machine):
            self.__machine = machine
            self.__type = state_type
            self.__input_tape = None
            self.__functions = []
            self.__auxiliary_tapes = []
            self.__output_tape = None

        def input_tape(self, tape):
            self.__input_tape = tape
            return self

        def function(self, function):
            self.__functions.append(function)
            return self

        def functions(self, functions):
            self.__functions = functions
            return self

        def auxiliary_tape(self, tape):
            self.__auxiliary_tapes.append(tape)
            return self

        def output_tape(self, tape):
            self.__output_tape = tape
            return self

        def build(self):
            return State(self.__machine, self.__type, self.__input_tape, self.__auxiliary_tapes, self.__output_tape,
                         self.__functions)


class ErrorState(State):

    def __init__(self, machine):
        super().__init__(machine, StateType.error, None, [], None, [])


class StateType(Enum):
    start = 0
    end = 1
    other = 2
    error = 3


class Function:

    def __init__(self, expected_inputs, outputs, move_directions, next_state=None):
        self.__next_state = next_state
        self.__expected_inputs = expected_inputs
        self.__outputs = outputs
        self.__move_directions = move_directions

    def matches(self, signs):
        return self.__expected_inputs == signs

    def apply(self, input_tape, auxiliary_tapes, output_tape):
        for out_tape, output in zip(auxiliary_tapes + [output_tape], self.__outputs):
            out_tape.write(output)
        for move_direction, tape in zip(self.__move_directions, [input_tape] + auxiliary_tapes + [output_tape]):
            tape.move(move_direction)
        return self.__next_state

    class Builder:
        def __init__(self):
            self.__next_state = None
            self.__expected_inputs = []
            self.__outputs = []
            self.__move_directions = []

        def next_state(self, next_state):
            self.__next_state = next_state
            return self

        def expected_input(self, input):
            self.__expected_inputs.append(input)
            return self

        def output(self, output):
            self.__outputs.append(output)
            return self

        def move_direction(self, move_direction):
            self.__move_directions.append(move_direction)
            return self

        def move_directions(self, move_directions):
            self.__move_directions = move_directions
            return self

        def build(self):
            return Function(self.__expected_inputs, self.__outputs, self.__move_directions, self.__next_state)


class TapeType(Enum):
    input = 0
    auxiliary = 1
    output = 2


class Tape:

    def __init__(self, type):
        self.__type = type
        self.__value = [EMPTY]
        self.__current_index = 0
        self.__direction_move = {
            Direction.left: self.__move_left,
            Direction.static: lambda: 0,
            Direction.right: self.__move_right
        }

    def value(self, value):
        self.__value = value + [EMPTY]

    def get_value(self):
        return self.__value

    def is_input(self):
        return self.__type == TapeType.input

    def is_output(self):
        return self.__type == TapeType.output

    def is_at_start(self):
        return self.__current_index == 0

    def is_at_end(self):
        return self.__value[self.__current_index] is EMPTY

    def read(self):
        return self.__value[self.__current_index]

    def write(self, sign):
        self.__value[self.__current_index] = sign

        if self.__current_index == len(self.__value) - 1:
            self.__value.append(EMPTY)

    def move(self, direction):
        self.__direction_move.get(direction)()

    def __move_left(self):
        if not self.is_at_start():
            self.__current_index -= 1

    def __move_right(self):
        self.__current_index += 1


class Direction(Enum):
    left = 0
    static = 1
    right = 2
