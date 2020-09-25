import ber_kompl.turing as tu


def build():
    input_tape = tu.Tape(tu.TapeType.input)
    output_tape = tu.Tape(tu.TapeType.output)

    machine = tu.Machine(input_tape)

    end_function = tu.Function.Builder().expected_input('0').output('0').move_directions(
        [tu.Direction.right, tu.Direction.right]).build()
    end_state = tu.State.Builder(tu.StateType.end, machine).input_tape(input_tape).output_tape(output_tape).function(
        end_function).build()

    to_end_function = tu.Function.Builder().expected_input('1').output(tu.EMPTY).move_directions(
        [tu.Direction.right, tu.Direction.static]).next_state(end_state).build()
    start_function = tu.Function.Builder().expected_input('0').output('0').move_directions(
        [tu.Direction.right, tu.Direction.right]).build()

    tu.State.Builder(tu.StateType.start, machine).input_tape(input_tape).output_tape(
        output_tape).functions([start_function, to_end_function]).build()

    return machine, output_tape
