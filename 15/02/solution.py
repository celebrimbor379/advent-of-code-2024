import argparse

def explore_vertical(direction, target_pos, boxes, walls, do_move):
    if target_pos not in boxes:
        return True
    
    left_pos = (target_pos[0] + direction, target_pos[1] - 1)
    center_pos = (target_pos[0] + direction, target_pos[1])
    right_pos = (target_pos[0] + direction, target_pos[1] + 1)
    
    if center_pos in walls or right_pos in walls:
        return False
    elif (explore_vertical(direction, left_pos, boxes, walls, do_move)
          and explore_vertical(direction, center_pos, boxes, walls, do_move)
          and explore_vertical(direction, right_pos, boxes, walls, do_move)):
        if do_move:
            boxes.remove(target_pos)
            boxes.add(center_pos)
        return True
    else:
        return False

def explore_horizontal(direction, target_pos, boxes, walls, do_move):
    if target_pos not in boxes:
        return True

    next_pos = (target_pos[0], target_pos[1] + direction)
    further_pos = (target_pos[0], target_pos[1] + (direction * 2))

    if (direction == 1 and further_pos in walls) or (direction == -1 and next_pos in walls):
        return False
    elif explore_horizontal(direction, further_pos, boxes, walls, do_move):
        if do_move:
            boxes.remove(target_pos)
            boxes.add(next_pos)
        return True
    else:
        return False

def do_move(move, robot, boxes, walls):
    # This does 2 depth-first searches for each move that isn't blocked: once to see if all the
    # boxes that would need to move can actually move, and a second one to walk the tree again and
    # actually move them. Would be more efficient to do a BFS I guess, but this works fine for this
    # size input.
    match move:
        case '^':
            north_pos = (robot[0] - 1, robot[1])
            nw_pos = (north_pos[0], north_pos[1] - 1)
            if (north_pos not in walls
                 and explore_vertical(-1, nw_pos, boxes, walls, do_move=False)
                 and explore_vertical(-1, north_pos, boxes, walls, do_move=False)):
                explore_vertical(-1, nw_pos, boxes, walls, do_move=True)
                explore_vertical(-1, north_pos, boxes, walls, do_move=True)
                return north_pos
        case 'v':
            south_pos = (robot[0] + 1, robot[1])
            sw_pos = (south_pos[0], south_pos[1] - 1)
            if (south_pos not in walls
                 and explore_vertical(1, sw_pos, boxes, walls, do_move=False)
                 and explore_vertical(1, south_pos, boxes, walls, do_move=False)):
                explore_vertical(1, sw_pos, boxes, walls, do_move=True)
                explore_vertical(1, south_pos, boxes, walls, do_move=True)
                return south_pos
        case '>':
            east_pos = (robot[0], robot[1] + 1)
            if east_pos not in walls and explore_horizontal(1, east_pos, boxes, walls, do_move=False):
                explore_horizontal(1, east_pos, boxes, walls, do_move=True)
                return east_pos
        case '<':
            west_pos = (robot[0], robot[1] - 1)
            more_west_pos = (robot[0], robot[1] - 2)
            if west_pos not in walls and explore_horizontal(-1, more_west_pos, boxes, walls, do_move=False):
                explore_horizontal(-1, more_west_pos, boxes, walls, do_move=True)
                return west_pos

    return robot

def calculate_gps_score(boxes):
    return sum([(row * 100) + col for row, col in boxes])

def get_solution(input_path):
    with open(input_path) as input_file:
        robot = None
        boxes = set()
        walls = set()
        moves = ''
        reading_grid = True

        for i, l in enumerate(input_file.readlines()):
            if l.strip() == '':
                reading_grid = False
            elif reading_grid:
                row = l.strip()
                for j in range(len(row)):
                    if row[j] == '#':
                        walls.add((i, j * 2))
                        walls.add((i, (j * 2) + 1))
                    elif row[j] == 'O':
                        boxes.add((i, j * 2))
                    elif row[j] == '@':
                        robot = (i, j * 2)
            else:
                moves += l.strip()

        for m in moves:
            robot = do_move(m, robot, boxes, walls)
        
    return calculate_gps_score(boxes)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path", help="Input file path")
    args = parser.parse_args()
    print(get_solution(args.input_path))

    
