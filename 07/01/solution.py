from pprint import pp
import argparse
from collections import deque

def compute_possible_outcomes(operands):
    queue = deque()
    queue.appendleft(operands[0])

    for op in operands[1:]:
        for i in range(len(queue)):
            n = queue.pop()
            queue.appendleft(n + op)
            queue.appendleft(n * op)

    return queue

def get_solution(input_path):
    result = 0
    
    with open(input_path) as input_file:
        for line in input_file:
            target, operands = line.strip().split(': ')
            target = int(target)
            operands = [int(x) for x in operands.split(' ')]
            if any([x == target for x in compute_possible_outcomes(operands)]):
                result += target

    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path", help="Input file path")
    args = parser.parse_args()
    print(get_solution(args.input_path))
