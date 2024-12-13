import argparse
from collections import deque

def on_grid(grid, pos):
    return pos[0] > -1 and pos[1] > -1 and pos[0] < len(grid) and pos[1] < len(grid[pos[0]])

def pos_matches_target(grid, pos, target_val):
    return on_grid(grid, pos) and grid[pos[0]][pos[1]] == target_val

def should_continue(grid, path, pos, next_val):
    return pos_matches_target(grid, pos, next_val) and (pos not in path)

def bfs(grid, pos):
    distinct_paths = 0
    queue = deque()
    queue.appendleft([pos])

    while len(queue) > 0:
        for _ in range(len(queue)):
            path = queue.pop()
            current_pos = path[len(path) - 1]
            
            if pos_matches_target(grid, current_pos, 9):
                distinct_paths += 1
            else:
                next_val = grid[current_pos[0]][current_pos[1]] + 1
                above = (current_pos[0] - 1, current_pos[1])
                right = (current_pos[0], current_pos[1] + 1)
                below = (current_pos[0] + 1, current_pos[1])
                left = (current_pos[0], current_pos[1] - 1)
                
                if should_continue(grid, path, above, next_val):
                    queue.appendleft(list(path + [above]))
                    
                if should_continue(grid, path, right, next_val):
                    queue.appendleft(list(path + [right]))
                    
                if should_continue(grid, path, below, next_val):
                    queue.appendleft(list(path + [below]))
                    
                if should_continue(grid, path, left, next_val):
                    queue.appendleft(list(path + [left]))

    return distinct_paths

def get_solution(input_path):
    result = 0

    with open(input_path) as input_file:
        grid = [[int(pos) for pos in line.strip()] for line in input_file]

        for i in range(len(grid)):
            line = grid[i]
            for j in range(len(line)):
                if grid[i][j] == 0:
                    result += bfs(grid, (i, j))

    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path", help="Input file path")
    args = parser.parse_args()
    print(get_solution(args.input_path))
