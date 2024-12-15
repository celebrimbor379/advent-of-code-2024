import argparse

def transform(stone):
    if stone == 0:
        return [1]
    elif len(str(stone)) % 2 == 0:
        chars = str(stone)
        mid = len(chars) // 2
        return [int(chars[:mid]), int(chars[mid:])]
    else:
        mult = stone * 2024
        return [mult]
        
def blink(stones, blinks):
    if blinks == 0:
        return stones

    transformed = []
    for s in stones:
        transformed += (transform(s))

    return blink(transformed, blinks - 1)
    

def get_solution(input_path):
    blinks = 25
    result = 0

    with open(input_path) as input_file:
        stones = [int(x) for x in input_file.readline().strip().split(' ')]
        return len(blink(stones, blinks))

    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path", help="Input file path")
    args = parser.parse_args()
    print(get_solution(args.input_path))
