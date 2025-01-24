import argparse
from functools import cache

@cache
def is_valid_candidate(candidate, patterns, start):
    if start == len(candidate):
        return 1

    return sum([is_valid_candidate(candidate, patterns, start + len(p)) for p in patterns
                if candidate[start:].startswith(p)])

def get_solution(input_path):
    with open(input_path) as input_file:
        p, _, *c = input_file.readlines()
        patterns = tuple(p.strip().split(', '))
        candidates = [x.strip() for x in c]
        
        return sum([is_valid_candidate(cand, patterns, 0) for cand in candidates])

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path", help="Input file path")
    args = parser.parse_args()
    print(get_solution(args.input_path))
