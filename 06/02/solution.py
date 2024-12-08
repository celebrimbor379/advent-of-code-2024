from pprint import pp
import argparse
from enum import Enum
import copy

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
    # pp('Entering loop check at {}, going direction {}, seen {}'.format(position, direction, seen))
    
    while position.on_grid(grid):
        # print(position)
        if (position.on_grid(grid)
            and (position in seen)
            and (direction in seen.get(position))):
        # pp('Found loop at {} in direction {} for condition {} and seen {}'.format(position, direction, (direction in seen.get(tuple(position))), seen.get(tuple(position))))
            return 1

        seen.setdefault(position, set()).add(direction)
        next_pos = position.inc(direction)
        
        if next_pos.on_grid(grid) and grid[next_pos.row][next_pos.col] == '#':
            direction = Direction.turn(direction)
            position = position.inc(direction)
        else:
            position = next_pos
                  
    return 0

def get_solution(input_path):
    result = 0
    sims = 0
    grid = []
    position = None
    direction = Direction.UP
    seen = {}

    with open(input_path) as input_file:
        for line in input_file:
            row = list(line.strip())
            if '^' in row:
                position = Position(len(grid), row.index('^'))
                row[row.index('^')] = '.'
            grid.append(row)

    # print()
    # print(position)
    # print(grid)

    while position.on_grid(grid):
        seen.setdefault(position, set()).add(direction)
        # pp(seen)
        next_pos = position.inc(direction)
        
        if next_pos.on_grid(grid) and grid[next_pos.row][next_pos.col] == '#':
            direction = Direction.turn(direction)
            position = position.inc(direction)
        else:
            branch_dir = Direction.turn(direction)
            branch_pos = position.inc(branch_dir)
            if (next_pos.on_grid(grid)
                and next_pos not in seen
                and branch_pos.on_grid(grid)
                and grid[branch_pos.row][branch_pos.col] != '#'):
                # sims += 1
                # print('sims={}'.format(sims))
                # pp('Seen before check {}'.format(seen))
                grid[next_pos.row][next_pos.col] = '#'
                x = check_for_loop(grid, branch_pos, copy.deepcopy(seen), branch_dir)
                grid[next_pos.row][next_pos.col] = '.'
                # x = check_for_loop(grid, branch_pos, seen, branch_dir)
                result += x
                # if x > 0:
                    # print('Result incremented to {}'.format(result))
                # pp('Seen after check {}'.format(seen))
            position = next_pos
    
    # for r in grid:
        # print(r)
    # print('Ran {} sims'.format(sims))
    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path", help="Input file path")
    args = parser.parse_args()
    print(get_solution(args.input_path))
