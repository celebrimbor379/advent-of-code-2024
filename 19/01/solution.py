import argparse

def is_valid_candidate(candidate, patterns, start):
    if start == len(candidate):
        return True

    for prefix in [p for p in patterns if candidate[start:].startswith(p)]:
        if is_valid_candidate(candidate, patterns, start + len(prefix)):
            return True

    return False

def get_solution(input_path):
    with open(input_path) as input_file:
        p, _, *c = input_file.readlines()
        patterns = p.strip().split(', ')
        candidates = [x.strip() for x in c]
        
        return sum([is_valid_candidate(c, patterns, 0) for c in candidates])

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path", help="Input file path")
    args = parser.parse_args()
    print(get_solution(args.input_path))
