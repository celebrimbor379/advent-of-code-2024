import argparse
from collections import deque

class Path():
    def __init__(self, visited, end, direction, total):
        self.visited = visited
        self.end = end
        self.direction = direction
        self.total = total

    def __str__(self):
        return 'end={}, direction={}, total={}, visited={}'.format(self.end, self.direction, self.total, self.visited)

def get_new_path(next_pos, next_direction, walls, cur, min_seen):
    if (not next_pos in walls) and (not next_pos in cur.visited):
        cost = cur.total + (1 if next_direction == cur.direction else 1001)
        if not cost >= min_seen:
            visited = set(cur.visited)
            visited.add(cur.end)
            return Path(visited, next_pos, next_direction, cost)
        
    return None
    

def find_lowest_cost(start, end, walls):
    min_seen = float('inf')
    queue = deque()
    queue.appendleft(Path(set(), start, 'E', 0))

    while len(queue) > 0:
        # print()
        for _ in range(len(queue)):
            cur = queue.pop()
            # print(cur)
            
            if cur.end == end:
                print('found end at {}'.format(cur))
                min_seen = min(min_seen, cur.total)
                continue

            east_path = get_new_path((cur.end[0], cur.end[1] + 1), 'E', walls, cur, min_seen)
            if east_path:
                queue.appendleft(east_path)
                
            west_path = get_new_path((cur.end[0], cur.end[1] - 1), 'W', walls, cur, min_seen)
            if west_path:
                queue.appendleft(west_path)
            
            north_path = get_new_path((cur.end[0] - 1, cur.end[1]), 'N', walls, cur, min_seen)
            if north_path:
                queue.appendleft(north_path)
            
            south_path = get_new_path((cur.end[0] + 1, cur.end[1]), 'S', walls, cur, min_seen)
            if south_path:
                queue.appendleft(south_path)
            
    return min_seen

def get_solution(input_path):
    walls = set()
    start = None
    end = None

    with open(input_path) as input_file:
        row = 0
        for line in input_file:
            l = line.strip()
            for col in range(len(l)):
                cur = l[col]
                match cur:
                    case '#':
                        walls.add((row, col))
                    case 'E':
                        end = (row, col)
                    case 'S':
                        start = (row, col)
            row += 1

        # print()
        # print(start)
        # print(end)
        # print(sorted(walls))

    return find_lowest_cost(start, end, walls)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path", help="Input file path")
    args = parser.parse_args()
    print(get_solution(args.input_path))
