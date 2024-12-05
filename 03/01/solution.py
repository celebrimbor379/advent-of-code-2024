import argparse
from enum import Enum

class States(Enum):
    BEG = 1
    MULT = 2
    OPEN_PARENS = 3
    FIRST_OPERAND = 4
    SECOND_OPERAND = 5
    CLOSE_PARENS = 6
    COMMA = 7

def parse_line(line):
    state = States.BEG
    i = 0
    pairs = []
    pair = None

    while i < len(line):
        match state:
            case States.BEG:
                while (i < len(line)) and line[i] != 'm':
                    i += 1
                state = States.MULT
            case States.MULT:
                if (i < len(line) - 2) and (line[i:i + 3] == 'mul'):
                    state = States.OPEN_PARENS
                    i += 3
                else:
                    state = States.BEG
                    i += 1
            case States.OPEN_PARENS:
                if (i < len(line)) and (line[i]) == '(':
                    state = States.FIRST_OPERAND
                    i += 1
                elif i < len(line):
                    state = States.BEG
            case States.FIRST_OPERAND:
                if (i < len(line)) and (line[i].isdigit()):
                    j = i + 1
                    while (j < len(line)) and line[j].isdigit():
                        j += 1
                    pair = [int(line[i:j])]
                    i = j
                    state = States.COMMA
                elif i < len(line):
                    state = States.BEG
            case States.COMMA:
                if (i < len(line)) and (line[i] == ','):
                    state = States.SECOND_OPERAND
                    i += 1
                elif i < len(line):
                    state = States.BEG
            case States.SECOND_OPERAND:
                if (i < len(line)) and (line[i].isdigit()):
                    j = i + 1
                    while (j < len(line)) and line[j].isdigit():
                        j += 1
                    pair.append(int(line[i:j]))
                    i = j
                    state = States.CLOSE_PARENS
                elif i < len(line):
                    state = States.BEG
            case States.CLOSE_PARENS:
                if (i < len(line)) and (line[i] == ')'):
                    pairs.append(pair)
                    i += 1
                    state = States.BEG
                elif i < len(line):
                    state = States.BEG
            case _:
                raise Exception('This should never happen!')
            
    return pairs

def get_solution(input_path):
    result = 0

    with open(input_path) as input_file:
        for line in input_file:
            products = parse_line(line)
            result += sum([x * y for x, y in products])

    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path", help="Input file path")
    args = parser.parse_args()
    print(get_solution(args.input_path))
