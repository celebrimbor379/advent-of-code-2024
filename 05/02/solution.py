import argparse
from functools import cmp_to_key

def sort_invalids(l, rules):
    # rules contains a mapping of all the numbers that can be considered "greater than" the key
    # (i.e. should come after it), so actually this is just a sorting problem
    def cmp_fn(a, b):
        return (a in rules and b in rules[a]) - (b in rules and a in rules[b])

    return sorted(l, key=cmp_to_key(cmp_fn))

def is_valid_update(update, rules):
    already_seen = set()

    # Check to see if anything to the left of this element is in a rule saying it should always be
    # to the right
    for x in update:
        if x in rules:
            for follower in rules[x]:
                if follower in already_seen:
                    return False
        already_seen.add(x)
    return True

def get_solution(input_path):
    finished_rules = False
    rules = {}
    lists = []

    with open(input_path) as input_file:
        for line in input_file:
            if line.strip() == '':
                finished_rules = True
            elif not finished_rules:
                k, v = [int(x) for x in line.strip().split('|')]
                rules.setdefault(k, []).append(v)
            else:
                lists.append([int(x) for x in line.strip().split(',')])

    return sum([x[len(x) // 2] for x in [sort_invalids(l, rules) for l in lists if not is_valid_update(l, rules)]])

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path", help="Input file path")
    args = parser.parse_args()
    print(get_solution(args.input_path))
