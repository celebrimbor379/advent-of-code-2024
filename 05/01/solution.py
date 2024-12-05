from pprint import pp
import argparse

def is_valid_update(update, rules):
    for i, page in enumerate(update):
        if page in rules:
            for antecedent in rules[page]:
                if (antecedent in update) and (not antecedent in update[0:i]):
                    return False
    return True

def get_solution(input_path):
    finished_rules = False
    rules = {}
    updates = []

    with open(input_path) as input_file:
        for line in input_file:
            if line.strip() == '':
                finished_rules = True
            elif not finished_rules:
                v, k = [int(x) for x in line.strip().split('|')]
                r = rules.get(k, [])
                r.append(v)
                rules[k] = r
            else:
                updates.append([int(x) for x in line.strip().split(',')])

    return sum([u[len(u) // 2] for u in updates if is_valid_update(u, rules)])

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path", help="Input file path")
    args = parser.parse_args()
    print(get_solution(args.input_path))
