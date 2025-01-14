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
    if neighbor_square and (direction in neighbor_square) and (not neighbor_square[direction].visited):
        neighbor = neighbor_square[direction]
        cost_from_current = current.cost + (1 if current.direction == direction else 1001)
        if cost_from_current < neighbor.cost:
            neighbor.cost = cost_from_current
            neighbor.parents.clear()
            neighbor.parents.append(current)
            heappush(pqueue, neighbor)
        elif cost_from_current == neighbor.cost:
            # Add all parents with an equal cost to collect all shortest paths
            neighbor.parents.append(current)

def go_go_gadget_dijkstra(start, nodes):
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
                process_neighbor('E', nodes[current.row][current.col + 1], pqueue, current)
                process_neighbor('N', nodes[current.row - 1][current.col], pqueue, current)
                process_neighbor('S', nodes[current.row + 1][current.col], pqueue, current)
            case 'W':
                process_neighbor('W', nodes[current.row][current.col - 1], pqueue, current)
                process_neighbor('N', nodes[current.row - 1][current.col], pqueue, current)
                process_neighbor('S', nodes[current.row + 1][current.col], pqueue, current)

def backtrack_from_end(node, seen):
    seen = {(node.row, node.col)}
    for p in node.parents:
        seen |= backtrack_from_end(p, seen)
    return seen

def get_solution(input_path):
    nodes = []
    start = None
    end = None

    with open(input_path) as input_file:
        row_num = 0
        for l in input_file:
            line = l.strip()
            # Store parsed nodes in a 2D array to make neighbor lookup easy
            row = [None] * len(line)
            for col_num in range(len(line)):
                match line[col_num]:
                    case '.':
                        # Since edge weights between two nodes are different depending on which
                        # direction the traveler is facing on the source node, we can just treat all
                        # row/column/direction combinations as distinct nodes.
                        row[col_num] = {'N': Node(float('inf'), row_num, col_num, 'N', False),
                                        'S': Node(float('inf'), row_num, col_num, 'S', False),
                                        'E': Node(float('inf'), row_num, col_num, 'E', False),
                                        'W': Node(float('inf'), row_num, col_num, 'W', False)}
                    case 'E':
                        # All input versions have 'E' in the upper right, so entrance directions can
                        # only be these two.
                        row[col_num] = {'N': Node(float('inf'), row_num, col_num, 'N', False),
                               'E': Node(float('inf'), row_num, col_num, 'E', False)}
                        end = row[col_num]
                    case 'S':
                        row[col_num] = {'E': Node(0, row_num, col_num, 'E', False)}
                        start = row[col_num]['E']
            nodes.append(row)
            row_num += 1

    go_go_gadget_dijkstra(start, nodes)
    tiles_on_shortest_paths = backtrack_from_end(end['N'] if end['N'].cost < end['E'].cost else end['E'], set())
    return len(tiles_on_shortest_paths)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path", help="Input file path")
    args = parser.parse_args()
    print(get_solution(args.input_path))
