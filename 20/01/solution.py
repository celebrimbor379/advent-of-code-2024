import argparse
from collections import defaultdict

def is_on_grid(pos, limit):
    return pos[0] > -1 and pos[1] > -1 and pos[0] < limit and pos[1] < limit

def get_neighbors(pos):
    return [(pos[0] - 1, pos[1]), (pos[0] + 1, pos[1]), (pos[0], pos[1] + 1), (pos[0], pos[1] - 1)]

def explore_wall(wall, grid, seen, source_distance):
    savings = []
    neighbors = get_neighbors(wall)

    for dest in [n for n in neighbors if is_on_grid(n, len(grid)) and (n not in seen) and (type(grid[n[0]][n[1]]) == int)]:
        diff = grid[dest[0]][dest[1]] - (source_distance + 2)
        if diff > 0:
            savings.append(diff)

    return savings

def map_out_cheats(start, grid):
    seen = set()
    savings = defaultdict(int)
    cur = start

    while cur:
        seen.add(cur)
        neighbors = get_neighbors(cur)
        
        for wall in [n for n in neighbors if grid[n[0]][n[1]] == '#']:
            for s in explore_wall(wall, grid, seen, grid[cur[0]][cur[1]]):
                savings[s] += 1
        
        cur = next((n for n in neighbors if n not in seen and type(grid[n[0]][n[1]]) == int), None)

    return savings

def scout_track(start, grid):
    cur = start
    distance = -1

    while cur:
        distance += 1
        grid[cur[0]][cur[1]] = distance
        neighbors = get_neighbors(cur)
        cur = next((n for n in neighbors if grid[n[0]][n[1]] == '.'), None)

def get_solution(input_path):
    with open(input_path) as input_file:
        grid = []
        start = None
        
        for x, row in enumerate(input_file):
            grid.append(list(row.strip()))
            
            start_idx = row.find('S')
            if start_idx > -1:
                grid[x][start_idx] = '.'
                start = (x, start_idx)
                
            end_idx = row.find('E')
            if end_idx > -1:
                grid[x][end_idx] = '.'
                
        scout_track(start, grid)
        return sum([v for k, v in map_out_cheats(start, grid).items() if k >= 100])

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path", help="Input file path")
    args = parser.parse_args()
    print(get_solution(args.input_path))
