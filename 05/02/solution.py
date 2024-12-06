from pprint import pp
import argparse
from functools import cmp_to_key

def aoc_sort(l, rules):
    # rules contains a mapping of all the numbers that can be considered "greater than" the key
    # (i.e. should come after it), so actually this is just a sorting problem
    def cmp_fn(a, b):
        return (b in rules and a in rules[b]) - (a in rules and b in rules[a])

    return sorted(l, key=cmp_to_key(cmp_fn))

def get_solution(input_path):
    result = 0
    rules = {}

    with open(input_path) as input_file:
        finished_rules = False
        for line in input_file:
            if line.strip() == '':
                finished_rules = True
            elif not finished_rules:
                k, v = [int(x) for x in line.strip().split('|')]
                rules.setdefault(k, []).append(v)
            else:
                l = [int(x) for x in line.strip().split(',')]
                sorted_l = aoc_sort(l, rules)
                if sorted_l != l:
                    result += sorted_l[len(sorted_l) // 2]

    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path", help="Input file path")
    args = parser.parse_args()
    print(get_solution(args.input_path))
