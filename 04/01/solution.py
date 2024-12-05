from pprint import pp
import argparse

CHARS = ['X', 'M', 'A', 'S']

def search_up(grid, row, col):
    pass

def dfs(grid, row, col, target_char, direction):
    if ((row < 0) or (row == len(grid))
        or (col < 0) or (col == len(grid[0]))
        or grid[row][col] != CHARS[target_char]):
        return 0
    elif target_char == 3:
        # print('found at {}, {}'.format(row, col))
        return 1
    else:
        return dfs(grid, row + direction[0], col + direction[1], target_char + 1, direction)

def get_solution(input_path):
    result = 0
    grid = []

    with open(input_path) as input_file:
        for line in input_file:
            grid.append(list(line.strip()))

    # print()
    # pp(grid)
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == 'X':
                # print('starting at {}, {}'.format(row, col))
                # print('total at {}, {} was {}'.format(row, col, total))
                # Clockwise roundy-round
                result += dfs(grid, row, col, 0, [-1, 0])
                result += dfs(grid, row, col, 0, [-1, 1])
                result += dfs(grid, row, col, 0, [0, 1])
                result += dfs(grid, row, col, 0, [1, 1])
                result += dfs(grid, row, col, 0, [1, 0])
                result += dfs(grid, row, col, 0, [1, -1])
                result += dfs(grid, row, col, 0, [0, -1])
                result += dfs(grid, row, col, 0, [-1, -1])
    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path", help="Input file path")
    args = parser.parse_args()
    print(get_solution(args.input_path))
