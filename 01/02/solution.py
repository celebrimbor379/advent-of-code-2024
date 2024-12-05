import argparse
import pprint

def get_solution(input_path):
    result = 0

    with open(input_path) as input_file:
        left = []
        right = {}

        for line in input_file:
            l, r = [int(x) for x in line.strip().split('   ')]
            left.append(l)
            right[r] = right.get(r, 0) + 1


        return sum([(lambda y: y * right.get(y, 0))(loc_id) for loc_id in left])

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path", help="Input file path")
    args = parser.parse_args()
    print(get_solution(args.input_path))
