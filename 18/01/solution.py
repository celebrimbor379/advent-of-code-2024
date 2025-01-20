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

def get_solution(input_path):
    with open(input_path) as input_file:
        positions = [x.split(',') for x in input_file.readlines()]
        obstacles = {(int(x), int(y)) for x, y in positions[:1024]}
        return bfs((0, 0), (70, 70), obstacles)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path", help="Input file path")
    args = parser.parse_args()
    print(get_solution(args.input_path))
