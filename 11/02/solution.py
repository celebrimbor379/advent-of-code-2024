import argparse
from functools import cache

def transform(stone):
    # pp(stone)
    if stone == 0:
        return [1]
    elif len(str(stone)) % 2 == 0:
        chars = str(stone)
        mid = len(chars) // 2
        return [int(chars[:mid]), int(chars[mid:])]
    else:
        mult = stone * 2024
        return [mult]
        
@cache
def blink(stone, blinks):
    transformed = transform(stone)
    # Don't actually need to compute the full transformed list, just need to sum up the number of
    # elements. Useful to think of it as DFS on a tree rather than manipulating arrays.
    if blinks == 1:
        return len(transformed)
    else:
        return sum([n for n in map(lambda s: blink(s, blinks - 1), transformed)])

def get_solution(input_path):
    blinks = 75
    result = 0

    with open(input_path) as input_file:
        stones = tuple([int(x) for x in input_file.readline().strip().split(' ')])
        return sum([n for n in map(lambda s: blink(s, blinks), stones)])

    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path", help="Input file path")
    args = parser.parse_args()
    print(get_solution(args.input_path))
