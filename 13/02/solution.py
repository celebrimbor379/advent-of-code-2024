import argparse
import re

def is_int(x):
    return x % 1 == 0

# This is Cramer's Rule. Thanks, Reddit.
def calculate_cost(a, b, prize):
    a_presses = ((prize[0] * b[1]) - (prize[1] * b[0])) / ((a[0] * b[1]) - (a[1] * b[0]))
    b_presses = ((a[0] * prize[1]) - (a[1] * prize[0])) / ((a[0] * b[1]) - (a[1] * b[0]))
    return (a_presses, b_presses) if (is_int(a_presses) and is_int(b_presses)) else (0, 0)

def get_solution(input_path):
    result = 0

    with open(input_path) as input_file:
        machines = [[tuple(map(int, re.findall('\\d+', section))) for section in machine.strip().split('\n')] for machine in input_file.read().split('\n\n')]

        for a, b, prize in machines:
            solution = calculate_cost(a, b, (prize[0] + 10000000000000, prize[1] + 10000000000000))
            result += solution[0] * 3
            result += solution[1]
        
    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path", help="Input file path")
    args = parser.parse_args()
    print(get_solution(args.input_path))
