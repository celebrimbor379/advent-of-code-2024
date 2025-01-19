import argparse
import re
from itertools import batched

def convert_combo(operand, machine):
    match operand:
        case 0 | 1 | 2 | 3:
            return operand
        case 4:
            return machine['reg_a']
        case 5:
            return machine['reg_b']
        case 6:
            return machine['reg_c']
        case _:
            raise Exception('Should never happen.')

def do_op(op, machine):
    op_code, operand = op

    match op_code:
        # adv / combo
        case 0:
            operand = convert_combo(operand, machine)
            machine['reg_a'] = machine['reg_a'] >> operand
            machine['pc'] += 1
        # bxl / literal
        case 1:
            machine['reg_b'] ^= operand
            machine['pc'] += 1
        # bst / combo
        case 2:
            machine['reg_b'] = convert_combo(operand, machine) % 8
            machine['pc'] += 1
        # jnz / literal
        case 3:
            machine['pc'] = operand if machine['reg_a'] != 0 else machine['pc'] + 1
        # bxc / ignores operand
        case 4:
            machine['reg_b'] ^= machine['reg_c']
            machine['pc'] += 1
        # out / combo
        case 5:
            operand = convert_combo(operand, machine) % 8
            machine['std_out'] += ',{}'.format(operand) if len(machine['std_out']) > 0 else str(operand)
            machine['pc'] += 1
        # bdv / combo
        case 6:
            operand = convert_combo(operand, machine)
            machine['reg_b'] = machine['reg_a'] >> operand
            machine['pc'] += 1
        # cdv / combo
        case 7:
            operand = convert_combo(operand, machine)
            machine['reg_c'] = machine['reg_a'] >> operand
            machine['pc'] += 1

# To get a feel for what's going on, run the "machine code" with different values starting in the A
# register, like 0-100. Look for patterns. Try printing everything as octal numbers instead of
# base-10.
#
# Since the value of the A register is shifted right by 3 bits (divided by 8) on every iteration,
# each digit in the output basically corresponds to an octal digit of the initial value of A. BUT,
# one of the instructions also uses part of the A register higher than the first 3 bits, so this is
# more complicated than just "print each octal digit". The only part of the output that isn't
# dependent on higher bits of A is the very last number, since at that point A ONLY has the lower
# three bits set. So we know there's only 8 possible values of the highest octal bit of A that can
# produce the last item in the output. So we start there, then recurse backwards through the output,
# shifting our candidate left each time to find a lower digit that works.
#
# Note that this solution only works for "programs" where the above properties are true, i.e. it
# will not work on the test input since that is a different set of instructions.
def derive_starting_value(instructions, expected_output, idx, x):
    # Base case: if we got here then we found a valid candidate for the lowest digit of A, thus our
    # solution
    if idx < 0:
        return x

    # This is basically a single left shift in octal, same as multiplying by 10 shifts everything
    # one place to the left in base 10.
    x = x << 3

    # Run the instruction set for every possible base-8 digit. If we're looking at the last item in
    # the output then skip 0 because that doesn't make any sense.
    for i in range(0, 8) if x > 0 else range(1, 8):
        candidate = x + i
        machine = {
            'pc': 0,
            'reg_a': candidate,
            'reg_b': 0,
            'reg_c': 0,
            'std_out': ''
        }

        # Only need to do one iteration since we only need one digit
        for instr in instructions:
            do_op(instr, machine)

        if (machine['std_out'] == expected_output[idx]):
            # Found a valid candidate for this digit, so recurse and see if there's a solution for
            # the rest using this one.
            result = derive_starting_value(instructions, expected_output, idx - 1, candidate)
            if result:
                return result
    
def get_solution(input_path):
    with open(input_path) as input_file:
        expected_output = [x for x in re.sub('[a-zA-Z: ]', '', input_file.readlines()[4].strip()).split(',')]
        instructions = list(batched([int(x) for x in expected_output], 2))
        return derive_starting_value(instructions, expected_output, len(expected_output) - 1, 0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path", help="Input file path")
    args = parser.parse_args()
    print(get_solution(args.input_path))
