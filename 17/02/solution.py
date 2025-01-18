import argparse
import re
from itertools import batched
from math import trunc

REG_A = 0
REG_B = 0
REG_C = 0
PC = 0
STD_OUT = ''

def convert_combo(operand):
    global REG_A
    global REG_B
    global REG_C
    
    match operand:
        case 0 | 1 | 2 | 3:
            return operand
        case 4:
            return REG_A
        case 5:
            return REG_B
        case 6:
            return REG_C
        case _:
            raise Exception('Should never happen.')

def do_op(op):
    global PC
    global REG_A
    global REG_B
    global REG_C
    global STD_OUT
    
    op_code, operand = op
    # print('op_code={}, operand={}'.format(op_code, operand))

    match op_code:
        # adv / combo
        case 0:
            operand = convert_combo(operand)
            # print('operand={}, denominator={}'.format(operand, pow(2, operand)))
            REG_A = REG_A >> operand
            return PC + 1
        # bxl / literal
        case 1:
            # print('XORing {} and {} gives {}'.format(REG_B, operand, REG_B ^ operand))
            REG_B ^= operand
            return PC + 1
        # bst / combo
        case 2:
            REG_B = convert_combo(operand) % 8
            return PC + 1
        # jnz / literal
        case 3:
            return operand if REG_A != 0 else PC + 1
        # bxc / ignores operand
        case 4:
            REG_B ^= REG_C
            return PC + 1
        # out / combo
        case 5:
            operand = convert_combo(operand) % 8
            # print('printing {}'.format(operand))
            STD_OUT += ',{}'.format(operand) if len(STD_OUT) > 0 else str(operand)
            return PC + 1
        # bdv / combo
        case 6:
            operand = convert_combo(operand)
            REG_B = REG_A >> operand
            return PC + 1
        # cdv / combo
        case 7:
            operand = convert_combo(operand)
            # print('operand={}, denominator={}'.format(operand, pow(2, operand)))
            REG_C = REG_A >> operand
            return PC + 1
    
    return PC + 1

def get_solution(input_path):
    global PC
    global REG_A
    global REG_B
    global REG_C
    global STD_OUT
    
    with open(input_path) as input_file:
        (a, b, c, _, instructions) = input_file.readlines()
        # REG_A = int(re.sub('[a-zA-Z: ]', '', a.strip()))
        # REG_B = int(re.sub('[a-zA-Z: ]', '', b.strip()))
        # REG_C = int(re.sub('[a-zA-Z: ]', '', c.strip()))
        # PC = 0
        # STD_OUT = ''
        
        instructions = list(batched([int(x) for x in re.sub('[a-zA-Z: ]', '', instructions.strip()).split(',')], 2))

        temp = ''
        print()
        for i in range(0,10):
        # for i in range(211106232532991, 211106232532993):
            
            REG_A = i
            REG_B = 0
            REG_C = 0
            PC = 0
            STD_OUT= ''
            
            while PC < len(instructions):
                PC = do_op(instructions[PC])

            # print(i)
            # temp += STD_OUT[0]
            print(STD_OUT)
            # if len(STD_OUT) == 31:
                # print(i)
                # print(STD_OUT)
                # break
        # print()
        # for i in range(0, len(temp), 8):
            # print(temp[i:i+8])

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path", help="Input file path")
    args = parser.parse_args()
    print(get_solution(args.input_path))
