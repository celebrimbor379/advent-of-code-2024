import argparse

def is_valid_pair(x, y, ascending):
    return x != y and ascending == (x < y) and abs(x - y) < 4

def is_safe(report):
    ascending = report[0] < report[1]

    for i in range(len(report) - 1):
        if not is_valid_pair(report[i], report[i + 1], ascending):
            return 0

    return 1

def get_solution(input_path):
    reports = []

    with open(input_path) as input_file:
        for line in input_file:
            reports.append([int(x) for x in line.strip().split(' ')])

    return sum([is_safe(x) for x in reports])

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path", help="Input file path")
    args = parser.parse_args()
    print(get_solution(args.input_path))
