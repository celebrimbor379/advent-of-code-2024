import argparse
import re

class Robot:
    def __init__(self, px, py, vx, vy):
        self.px = int(px)
        self.py = int(py)
        self.vx = int(vx)
        self.vy = int(vy)

    def __str__(self):
        return 'px={}, py={}, vx={}, vy={}'.format(self.px, self.py, self.vx, self.vy)

def parse_line(line):
    px, py, vx, vy = [x for x in re.findall('-?\\d+', line)]
    return Robot(px, py, vx, vy)

def get_solution(input_path):
    width = 101
    height = 103
    cycles = 10000

    with open(input_path) as input_file:
        robots = [parse_line(line) for line in input_file]

        for i in range(1, cycles):
            grid = [list('.') * width for i in range(height)]
            
            for r in robots:
                r.px = (r.vx + r.px) % width
                r.py = (r.vy + r.py) % height
                grid[r.py][r.px] = 'X'

            if any([x for x in grid if re.search('XXXXXXXXXXXXXXX', ''.join(x))]):
                print('\n------------------------------------------------------------')
                print('\ncycle={}'.format(i))
                for row in grid:
                    print(''.join(row))
            
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path", help="Input file path")
    args = parser.parse_args()
    print(get_solution(args.input_path))
