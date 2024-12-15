import argparse
from collections import deque

def is_off_grid(pos, grid):
    return pos[0] < 0 or pos[1] < 0 or pos[0] >= len(grid) or pos[1] >= len(grid[0])

def not_in_region(pos, grid, target_value):
    return is_off_grid(pos, grid) or grid[pos[0]][pos[1]] != target_value

def explore_region(pos, grid):
    queue = deque()
    seen = set()
    perimiter = 0
    target_val = grid[pos[0]][pos[1]]
    
    queue.appendleft(pos)
    seen.add(pos)

    while len(queue) > 0:
        cur = queue.pop()
        above = (cur[0] - 1, cur[1])
        below = (cur[0] + 1, cur[1])
        right = (cur[0], cur[1] + 1)
        left = (cur[0], cur[1] - 1)
        
        if not_in_region(above, grid, target_val):
            perimiter += 1
        elif above not in seen:
            seen.add(above)
            queue.appendleft(above)
            
        if not_in_region(below, grid, target_val):
            perimiter += 1
        elif below not in seen:
            seen.add(below)
            queue.appendleft(below)
            
        if not_in_region(right, grid, target_val):
            perimiter += 1
        elif right not in seen:
            seen.add(right)
            queue.appendleft(right)
            
        if not_in_region(left, grid, target_val):
            perimiter += 1
        elif left not in seen:
            seen.add(left)
            queue.appendleft(left)

    return (seen, perimiter)

def get_solution(input_path):
    with open(input_path) as input_file:
        result = 0
        grid = [[x for x in row.strip()] for row in input_file.readlines()]
        explored = set()

        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if (i, j) not in explored:
                    region = explore_region((i, j), grid)
                    result += len(region[0]) * region[1]
                    explored |= region[0]

        return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path", help="Input file path")
    args = parser.parse_args()
    print(get_solution(args.input_path))
