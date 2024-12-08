import argparse
from enum import Enum

class Position:
    row = 0
    col = 0

    def __init__(self, row, col):
        self.row = row
        self.col = col

    def __str__(self):
       return '({}, {})'.format(self.row, self.col)

    def __eq__(self, other):
       return other and self.row == other.row and self.col == other.col

    def __hash__(self):
       return hash((self.row, self.col))

    def inc(self, direction):
        return Position(self.row + direction.value[0], self.col + direction.value[1])

    def on_grid(self, grid):
        return (self.row > -1
        and self.col > -1
        and self.row < len(grid)
        and self.col < len(grid[0]))

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

def check_for_loop(grid, position, seen, direction):
    while position.on_grid(grid):
        next_pos = position.inc(direction)

        if next_pos.on_grid(grid) and grid[next_pos.row][next_pos.col] == '#':
            if (position in seen) and (direction in seen[position]):
                return 1
            else:
                seen.setdefault(position, set()).add(direction)
                direction = Direction.turn(direction)
        else:
            position = next_pos
    
    return 0

def get_solution(input_path):
    result = 0
    grid = []
    start = None
    position = None
    direction = Direction.UP
    seen = set()

    with open(input_path) as input_file:
        for line in input_file:
            row = list(line.strip())
            if '^' in row:
                start = Position(len(grid), row.index('^'))
                row[row.index('^')] = '.'
            grid.append(row)

    position = start.inc(direction)

    while position.on_grid(grid):
        next_pos = position.inc(direction)
        
        if next_pos.on_grid(grid) and grid[next_pos.row][next_pos.col] == '#':
            direction = Direction.turn(direction)
        else:
            seen.add(position)
            position = next_pos

    for s in seen:
        grid[s.row][s.col] = '#'
        position = start
        result += check_for_loop(grid, position, {}, Direction.UP)
        grid[s.row][s.col] = '.'

    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path", help="Input file path")
    args = parser.parse_args()
    print(get_solution(args.input_path))
