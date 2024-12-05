import argparse
import pprint

def get_solution(input_path):
    result = 0

    with open(input_path) as input_file:
        left = []
        right = []
        
        for line in input_file:
            items = line.strip().split('   ')
            left.append(int(items[0]))
            right.append(int(items[1]))

        left.sort()
        right.sort()
        
        # print(left)
        # print(right)

        for i in range(len(left)):
            result += abs(left[i] - right[i])

    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path", help="Input file path")
    args = parser.parse_args()
    print(get_solution(args.input_path))
