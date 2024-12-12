import argparse

CHARS = ['M', 'A', 'S']

# The name "dfs" is totally wrong here. Left over from when I thought the reqs were to do a zig-zag
# search, but it's closing in on 10pm and I'm sleepy so eff it.
def dfs(grid, row, col, target_char, direction):
    if ((row < 0) or (row == len(grid))
        or (col < 0) or (col == len(grid[0]))
        or grid[row][col] != CHARS[target_char]):
        return False
    elif target_char == 2:
        return True
    else:
        return dfs(grid, row + direction[0], col + direction[1], target_char + 1, direction)

def get_solution(input_path):
    result = 0
    grid = []

    with open(input_path) as input_file:
        for line in input_file:
            grid.append(list(line.strip()))

    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == 'A':
                if ( (dfs(grid, row - 1, col - 1, 0, [1, 1]) or dfs(grid, row + 1, col + 1, 0, [-1, -1]))
                    and (dfs(grid, row - 1, col + 1, 0, [1, -1]) or dfs(grid, row + 1, col - 1, 0, [-1, 1])) ):
                    result += 1
                
    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path", help="Input file path")
    args = parser.parse_args()
    print(get_solution(args.input_path))
