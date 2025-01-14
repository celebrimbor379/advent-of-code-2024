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
    
def get_solution(input_path):
    with open(input_path) as input_file:
        pattern = '[a-zA-Z: ]'
        machine = {
            'pc': 0,
            'reg_a': 0,
            'reg_b': 0,
            'reg_c': 0,
            'std_out': ''
        }
        (a, b, c, _, instructions) = input_file.readlines()
        machine['reg_a'] = int(re.sub(pattern, '', a.strip()))
        machine['reg_b'] = int(re.sub(pattern, '', b.strip()))
        machine['reg_c'] = int(re.sub(pattern, '', c.strip()))
        instructions = list(batched([int(x) for x in re.sub('[a-zA-Z: ]', '', instructions.strip()).split(',')], 2))

        while machine['pc'] < len(instructions):
            do_op(instructions[machine['pc']], machine)

    return machine['std_out']

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path", help="Input file path")
    args = parser.parse_args()
    print(get_solution(args.input_path))
