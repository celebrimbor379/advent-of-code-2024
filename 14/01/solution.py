import argparse
import re

class Robot:
    def __init__(self, px, py, vx, vy):
        self.px = int(px)
        self.py = int(py)
        self.vx = int(vx)
        self.vy = int(vy)

def parse_line(line):
    px, py, vx, vy = [x for x in re.findall('-?\\d+', line)]
    return Robot(px, py, vx, vy)

def get_solution(input_path):
    width = 101
    height = 103
    cycles = 100
    mid_x = width // 2
    mid_y = height // 2
    quadrants = {'nw': 0, 'ne': 0, 'se': 0, 'sw': 0}

    with open(input_path) as input_file:
        for robot in [parse_line(line) for line in input_file]:
            robot.px = ((cycles * robot.vx) + robot.px) % width
            robot.py = ((cycles * robot.vy) + robot.py) % height
            
            if robot.px != mid_x and robot.py != mid_y:
                quadrant = 'n' if robot.py < mid_y else 's'
                quadrant += 'w' if robot.px < mid_x else 'e'
                quadrants[quadrant] += 1

    return quadrants['nw'] * quadrants['ne'] * quadrants['se'] * quadrants['sw']

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path", help="Input file path")
    args = parser.parse_args()
    print(get_solution(args.input_path))
