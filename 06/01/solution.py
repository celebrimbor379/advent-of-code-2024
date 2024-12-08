import argparse
from enum import Enum

class Direction(Enum):
    UP = (-1, 0)
    RIGHT = (0, 1)
    DOWN = (1, 0)
    LEFT = (0, -1)

    def turn(direction):
        match direction:
            case Direction.UP:
                return Direction.RIGHT
            case Direction.RIGHT:
                return Direction.DOWN
            case Direction.DOWN:
                return Direction.LEFT
            case Direction.LEFT:
                return Direction.UP

def is_on_grid(grid, position):
    return (position[0] > -1
            and position[1] > -1
            and position[0] < len(grid)
            and position[1] < len(grid[0]))

def inc_position(position, direction):
    return [position[0] + direction.value[0], position[1] + direction.value[1]]

def get_solution(input_path):
    result = 0
    grid = []
    position = [0,0]
    direction = Direction.UP

    with open(input_path) as input_file:
        for line in input_file:
            row = list(line.strip())
            grid.append(row)
            if '^' in row:
                position = [len(grid) - 1, row.index('^')]

    while is_on_grid(grid, position):
        next_pos = inc_position(position, direction)
        if is_on_grid(grid, next_pos) and grid[next_pos[0]][next_pos[1]] == '#':
            direction = Direction.turn(direction)
        else:
            if not grid[position[0]][position[1]] == 'X':
                result += 1
            grid[position[0]][position[1]] = 'X'
            position = next_pos
    
    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path", help="Input file path")
    args = parser.parse_args()
    print(get_solution(args.input_path))
