import argparse
from itertools import groupby, combinations

def is_on_grid(pos, grid):
    return pos[0] > -1 and pos[1] > -1 and pos[0] < len(grid) and pos[1] < len(grid[0])

def get_antinodes(upper, lower, grid):
    result = []
    delta = (lower[0] - upper[0], lower[1] - upper[1])
    upper_antinode = (upper[0] - delta[0], upper[1] - delta[1])
    lower_antinode = (lower[0] + delta[0], lower[1] + delta[1])
    
    if is_on_grid(upper_antinode, grid):
        result.append(upper_antinode)
    if is_on_grid(lower_antinode, grid):
        result.append(lower_antinode)
        
    return result

def get_solution(input_path):
    with open(input_path) as input_file:
        grid = [[y for y in x.strip()] for x in input_file]

    # Why not make this as unreadable as possible to get it down to as few lines as possible?
    # Otherwise it might as well be Java, right? Here it is in plain English:
    
    # Collect all coordinates that have an antenna, along with the label of the antenna
    # itself. Sorting by label is important so we can groupby in the next step (Python is weird).
    antennas = sorted([(i, j, label) for i, row in enumerate(grid) for j, label in enumerate(row) if label != '.'], key=lambda x: x[2])
    # Collect all combinations of 2 antennas that have the same name.
    pairs = [(upper, lower) for key, group in groupby(antennas, lambda x: x[2]) for upper, lower in combinations(group, 2)]
    # Compute the antinodes for each pair that are actually on the board and return the number of unique ones.
    return len({a for upper, lower in pairs for a in get_antinodes(upper, lower, grid)})

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path", help="Input file path")
    args = parser.parse_args()
    print(get_solution(args.input_path))
