from pprint import pp
import argparse

def get_solution(input_path):
    result = 0

    with open(input_path) as input_file:
        for line in input_file:
            pass

    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path", help="Input file path")
    args = parser.parse_args()
    print(get_solution(args.input_path))
