import argparse
from dataclasses import dataclass, field

@dataclass(unsafe_hash=True, order=True)
class PathNode:
    row: int
    col: int
    visited: bool = field(hash=False, compare=False, default=False)
    next: 'PathNode' = field(hash=False, compare=False, default=False)
    distance: int = field(hash=False, compare=False, default=0)

def walk_full_path():
    pass

def get_solution(input_path):
    result = 0
    with open(input_path) as input_file:
        walls = set()
        path_nodes = set()
        start = None
        end = None
        for row, line in enumerate(input_file):
            for col, c in enumerate(line):
                pos = (row, col)
                match c:
                    case '#':
                        walls.add(pos)
                    case 'S':
                        start = pos
                    case 'E':
                        end = pos
                    case '.':
                        path_nodes.add(PathNode(row, col))

        print()
        # for n in sorted(path_nodes):
            # print(n)
        # print('start={}, end={}'.format(start, end))
                

    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path", help="Input file path")
    args = parser.parse_args()
    print(get_solution(args.input_path))
