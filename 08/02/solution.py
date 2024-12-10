import argparse
from itertools import groupby, combinations
from operator import add, sub

def on_grid(pos, grid):
    return pos[0] > -1 and pos[1] > -1 and pos[0] < len(grid) and pos[1] < len(grid[0])

def fan_out(pos, delta, grid, op):
    if not on_grid(pos, grid):
        return set()
    
    new_pos = (op(pos[0], delta[0]), op(pos[1], delta[1]))
    return {pos} | fan_out(new_pos, delta, grid, op)

def get_antinodes(upper, lower, grid):
    delta = (lower[0] - upper[0], lower[1] - upper[1])
    return fan_out((upper[0], upper[1]), delta, grid, sub) | fan_out((lower[0], lower[1]), delta, grid, add)

def get_solution(input_path):
    with open(input_path) as input_file:
        grid = [[y for y in x.strip()] for x in input_file]
        antennas = sorted([(i, j, freq) for i, row in enumerate(grid) for j, freq in enumerate(row) if freq != '.'], key=lambda x: x[2])
        pairs = [(upper, lower) for key, group in groupby(antennas, lambda x: x[2]) for upper, lower in combinations(group, 2)]
        return len({a for upper, lower in pairs for a in get_antinodes(upper, lower, grid)})

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path", help="Input file path")
    args = parser.parse_args()
    print(get_solution(args.input_path))
