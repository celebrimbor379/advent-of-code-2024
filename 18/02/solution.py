import argparse
from collections import deque


def is_off_grid(pos, limit):
    x, y = pos
    return x < 0 or y < 0 or x > limit or y > limit

def process_neighbor(neighbor, obstacles, seen, limit, q):
    if (not neighbor in obstacles) and (not neighbor in seen) and (not is_off_grid(neighbor, limit)):
        q.appendleft(neighbor)
        seen.add(neighbor)
    
def bfs(start, end, obstacles):
    q = deque()
    seen = set()
    distance = 0
    limit = end[0]

    q.appendleft(start)
    seen.add(start)

    while q:
        for _ in range(len(q)):
            cur = q.pop()
            
            if cur == end:
                return distance
            
            process_neighbor((cur[0], cur[1] - 1), obstacles, seen, limit, q)
            process_neighbor((cur[0], cur[1] + 1), obstacles, seen, limit, q)
            process_neighbor((cur[0] + 1, cur[1]), obstacles, seen, limit, q)
            process_neighbor((cur[0] - 1, cur[1]), obstacles, seen, limit, q)
            
        distance += 1

def find_first_bad_position(positions, grid_size):
    left = 0
    right = len(positions) - 1

    while left <= right:
        mid = left + ((right - left) // 2)
        obstacles = {(x, y) for x, y in positions[:mid + 1]}
        search_result = bfs((0,0), (grid_size, grid_size), obstacles)

        # Looking for the first element that does NOT have a valid path through the grid
        if search_result:
            left = mid + 1
        else:
            right = mid - 1

    return positions[right + 1]
        
def get_solution(input_path):
    with open(input_path) as input_file:
        grid_size = 70
        positions = [[int(y) for y in x.strip().split(',')] for x in input_file.readlines()]
        result = find_first_bad_position(positions, grid_size)
        return '{},{}'.format(result[0], result[1])

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path", help="Input file path")
    args = parser.parse_args()
    print(get_solution(args.input_path))
