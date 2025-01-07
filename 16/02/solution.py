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

def process_neighbor(direction, neighbor_square, pqueue, current):
    if neighbor_square and direction in neighbor_square and not neighbor_square[direction].visited:
        neighbor = neighbor_square[direction]
        cost_from_current = current.cost + (1 if current.direction == direction else 1001)
        if cost_from_current < neighbor.cost:
            neighbor.cost = cost_from_current
            neighbor.parents.clear()
            neighbor.parents.append(current)
            heappush(pqueue, neighbor)
        elif cost_from_current == neighbor.cost:
            # Add all parents with an equal cost
            neighbor.parents.append(current)

def go_go_gadget_dijkstra(start, nodes):
    # heapq implements heap operations on a plain ol' list, no actual heap needed.
    pqueue = []
    heappush(pqueue, start)

    while pqueue:
        current = heappop(pqueue)
        current.visited = True
        match current.direction:
            case 'N':
                process_neighbor('N', nodes[current.row - 1][current.col], pqueue, current)
                process_neighbor('E', nodes[current.row][current.col + 1], pqueue, current)
                process_neighbor('W', nodes[current.row][current.col - 1], pqueue, current)
            case 'S':
                process_neighbor('S', nodes[current.row + 1][current.col], pqueue, current)
                process_neighbor('E', nodes[current.row][current.col + 1], pqueue, current)
                process_neighbor('W', nodes[current.row][current.col - 1], pqueue, current)
            case 'E':
                process_neighbor('N', nodes[current.row - 1][current.col], pqueue, current)
                process_neighbor('S', nodes[current.row + 1][current.col], pqueue, current)
                process_neighbor('E', nodes[current.row][current.col + 1], pqueue, current)
            case 'W':
                process_neighbor('N', nodes[current.row - 1][current.col], pqueue, current)
                process_neighbor('S', nodes[current.row + 1][current.col], pqueue, current)
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
                        row[col_num] = {'N': Node(float('inf'), row_num, col_num, 'N', False),
                                        'S': Node(float('inf'), row_num, col_num, 'S', False),
                                        'E': Node(float('inf'), row_num, col_num, 'E', False),
                                        'W': Node(float('inf'), row_num, col_num, 'W', False)}
                    case 'E':
                        end = {'N': Node(float('inf'), row_num, col_num, 'N', False),
                               'E': Node(float('inf'), row_num, col_num, 'E', False)}
                        row[col_num] = end
                    case 'S':
                        row[col_num] = {'E': Node(0, row_num, col_num, 'E', False)}
                        start = row[col_num]['E']
            nodes.append(row)
            row_num += 1

    go_go_gadget_dijkstra(start, nodes)
    tiles = set()
    walk_path(sorted(end.values(), key=lambda x: x.cost)[0], tiles)

    print()
    for t in tiles:
        raw[t[0]][t[1]] = 'O'
    for r in raw:
        print(''.join(r))
    
    return len(tiles)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path", help="Input file path")
    args = parser.parse_args()
    print(get_solution(args.input_path))
