import argparse
from collections import deque
from itertools import groupby, pairwise
from operator import itemgetter

def is_off_grid(pos, grid):
    return pos[0] < 0 or pos[1] < 0 or pos[0] >= len(grid) or pos[1] >= len(grid[0])

def not_in_region(pos, grid, target_value):
    return is_off_grid(pos, grid) or grid[pos[0]][pos[1]] != target_value

# Each distinct non-contiguous sequence of positions in the same column counts as a separate "side",
# so here we operate on a set of coordinates all "facing" the same way (left or right), group them
# by column (all in the same vertical column, but not necessarily an unbroken sequence), then count
# the number of times there's a break in the ascending sequence of rows. This is easier to
# understand visually, so recommend looking at the test data.
def count_vertical_sides(positions):
    sides = 0
    positions = sorted(positions, key=itemgetter(1, 0))
    
    for key, col in groupby(positions, key=itemgetter(1)):
        sides += 1
        sides += len([row_pair for row_pair in pairwise([c[0] for c in col]) if row_pair[1] - row_pair[0] != 1])

    return sides

# Yes this code is repetitive, no I don't care right now.
def count_horizontal_sides(positions):
    sides = 0
    positions = sorted(positions, key=itemgetter(0, 1))
    
    for key, row in groupby(positions, key=itemgetter(0)):
        sides += 1
        sides += len([col_pair for col_pair in pairwise([r[1] for r in row]) if col_pair[1] - col_pair[0] != 1])

    return sides

def compute_num_sides(perimeter):
    return (count_horizontal_sides(perimeter['UP'])
            + count_horizontal_sides(perimeter['DOWN'])
            + count_vertical_sides(perimeter['LEFT'])
            + count_vertical_sides(perimeter['RIGHT']))

def explore_region(pos, grid):
    queue = deque()
    area = set()
    perimiter = {}
    target_val = grid[pos[0]][pos[1]]
    
    queue.appendleft(pos)
    area.add(pos)

    while len(queue) > 0:
        cur = queue.pop()
        above = (cur[0] - 1, cur[1])
        below = (cur[0] + 1, cur[1])
        right = (cur[0], cur[1] + 1)
        left = (cur[0], cur[1] - 1)
        
        if not_in_region(above, grid, target_val):
            perimiter.setdefault('UP', set()).add((cur[0], cur[1]))
        elif above not in area:
            area.add(above)
            queue.appendleft(above)
            
        if not_in_region(below, grid, target_val):
            perimiter.setdefault('DOWN', set()).add((cur[0], cur[1]))
        elif below not in area:
            area.add(below)
            queue.appendleft(below)
            
        if not_in_region(right, grid, target_val):
            perimiter.setdefault('RIGHT', set()).add((cur[0], cur[1]))
        elif right not in area:
            area.add(right)
            queue.appendleft(right)
            
        if not_in_region(left, grid, target_val):
            perimiter.setdefault('LEFT', set()).add((cur[0], cur[1]))
        elif left not in area:
            area.add(left)
            queue.appendleft(left)

    return (area, perimiter)

def get_solution(input_path):
    with open(input_path) as input_file:
        result = 0
        grid = [[x for x in row.strip()] for row in input_file.readlines()]
        explored = set()

        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if (i, j) not in explored:
                    region = explore_region((i, j), grid)
                    result += len(region[0]) * compute_num_sides(region[1])
                    explored |= region[0]

        return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path", help="Input file path")
    args = parser.parse_args()
    print(get_solution(args.input_path))
