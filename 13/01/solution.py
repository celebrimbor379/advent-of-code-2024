from pprint import pp
import argparse
import re
from functools import cache

def increment_position(start, inc):
    return (start[0] + inc[0], start[1] + inc[1])

@cache
def find_cheapest_path(start, a, b, prize):
    if start[0] == prize[0] and start[1] == prize[1]:
        return 0
    elif start[0] > prize[0] or start[1] > prize[1]:
        return float('inf')
    else:
        return min(3 + find_cheapest_path(increment_position(start, a), a, b, prize),
                   1 + find_cheapest_path(increment_position(start, b), a, b, prize))

def get_solution(input_path):
    result = 0

    with open(input_path) as input_file:
        machines = [[tuple(map(int, re.findall('\\d+', section))) for section in machine.strip().split('\n')] for machine in input_file.read().split('\n\n')]
        print()
        # pp(machines)

        for a, b, prize in machines:
            cost = find_cheapest_path((0, 0), a, b, prize)
            print('a={}, b={}, prize={}, lowest_cost={}'.format(a, b, prize, cost))
            result += cost if cost != float('inf') else 0
            
    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path", help="Input file path")
    args = parser.parse_args()
    print(get_solution(args.input_path))
