import argparse
from heapq import heappush, heappop
from dataclasses import dataclass, field

@dataclass(order=True)
class Node:
    cost: int
    row: int
    col: int
    direction: str
    visited: bool
    parents: list = field(default_factory=list)

def process_neighbor(direction, neighbor, pqueue, current):
    if neighbor:
        cost_from_current = current.cost + (1 if current.direction == direction else 1001)
        if neighbor.visited and neighbor.cost == cost_from_current:
            # This node has more than one shortest path to it, so we need to keep references to all of them
            neighbor.parents.append(current)
        elif not neighbor.visited:
            neighbor.direction = direction
            neighbor.cost = min(neighbor.cost, cost_from_current)
            # Update the parent along with the cost until the node is actually visited.
            neighbor.parents.clear()
            neighbor.parents.append(current)
            heappush(pqueue, neighbor)

def go_go_gadget_dijkstra(start, nodes):
    # heapq implements heap operations on a plain ol' list, no actual heap needed. This will be our
    # priority queue. Sort key will be the cost since @dataclasses are compared using their fields
    # as a tuple, in order.
    pqueue = []
    heappush(pqueue, start)

    while len(pqueue) > 0:
        current = heappop(pqueue)
        current.visited = True
        process_neighbor('N', nodes[current.row - 1][current.col], pqueue, current)
        process_neighbor('S', nodes[current.row + 1][current.col], pqueue, current)
        process_neighbor('E', nodes[current.row][current.col + 1], pqueue, current)
        process_neighbor('W', nodes[current.row][current.col - 1], pqueue, current)

def walk_path(node, seen):
    if not node:
        return
    
    seen.add((node.row, node.col))
    for p in node.parents:
        walk_path(p, seen)
        
def get_solution(input_path):
    raw = []
    nodes = []
    start = None
    end = None

    with open(input_path) as input_file:
        row_num = 0
        for l in input_file:
            line = l.strip()
            raw.append(list(line))
            # Store parsed nodes in a 2D array to make neighbor lookup easy
            row = [None] * len(line)
            for col_num in range(len(line)):
                match line[col_num]:
                    case '.':
                        row[col_num] = Node(float('inf'), row_num, col_num, '', False)
                    case 'E':
                        end = Node(float('inf'), row_num, col_num, '', False)
                        row[col_num] = end
                    case 'S':
                        start = Node(0, row_num, col_num, 'E', False)
                        row[col_num] = start
            nodes.append(row)
            row_num += 1

    go_go_gadget_dijkstra(start, nodes)
    tiles = set()
    walk_path(end, tiles)

    for t in tiles:
        raw[t[0]][t[1]] = 'O'
    print()
    for r in raw:
        print(''.join(r))

    print(sorted(tiles))

    for row in nodes:
        for n in row:
            if n and (n.row, n.col) == (7, 4):
                print(n)
            if n and (n.row, n.col) == (7, 5):
                print(n)
    
    return len(tiles)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path", help="Input file path")
    args = parser.parse_args()
    print(get_solution(args.input_path))
