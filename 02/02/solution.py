import argparse

def is_valid_pair(report, i, j, ascending):
    diff = report[i] - report[j]
    return diff != 0 and ascending == (diff < 0) and abs(diff) < 4

def is_safe(report, already_replaced=False):
    ascending = report[0] < report[1]
    for i in range(len(report) - 1):
        if not is_valid_pair(report, i, i + 1, ascending):
            return (not already_replaced) and (is_safe(report[0:i - 1] + report[i:], True)
                                               or is_safe(report[0:i] + report[i + 1:], True)
                                               or is_safe(report[0:i + 1] + report[i + 2:], True))

    return True

def get_solution(input_path):
    reports = []
    scores = []

    with open(input_path) as input_file:
        for line in input_file:
            reports.append([int(x) for x in line.strip().split(' ')])

        for r in reports:
            scores.append(is_safe(r))

    return sum([int(x) for x in scores])

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path", help="Input file path")
    args = parser.parse_args()
    print(get_solution(args.input_path))
