import argparse

def do_move(move, grid, robot):
    destination = None

    match move:
        case '<':
            next_pos = (robot[0], robot[1] - 1)
            if grid[next_pos[0]][next_pos[1]] == '#':
                destination = robot
            elif grid[next_pos[0]][next_pos[1]] == '.':
                destination = next_pos
            else:
                row = grid[robot[0]]
                swap_dest = next_pos[1]
                while swap_dest > -1 and row[swap_dest] not in '.#':
                    swap_dest -= 1
                if swap_dest == -1 or row[swap_dest] == '#':
                    destination = robot
                else:
                    row[swap_dest] = 'O'
                    row[next_pos[1]] = '.'
                    destination = next_pos
        case 'v':
            next_pos = (robot[0] + 1, robot[1])
            if grid[next_pos[0]][next_pos[1]] == '#':
                destination = robot
            elif grid[next_pos[0]][next_pos[1]] == '.':
                destination = next_pos
            else:
                swap_dest = next_pos[0]
                col = next_pos[1]
                while swap_dest < len(grid) and grid[swap_dest][col] not in '.#':
                    swap_dest += 1
                if swap_dest == len(grid) or grid[swap_dest][col] == '#':
                    destination = robot
                else:
                    grid[swap_dest][col] = 'O'
                    grid[next_pos[0]][next_pos[1]] = '.'
                    destination = next_pos
        case '^':
            next_pos = (robot[0] - 1, robot[1])
            if grid[next_pos[0]][next_pos[1]] == '#':
                destination = robot
            elif grid[next_pos[0]][next_pos[1]] == '.':
                destination = next_pos
            else:
                swap_dest = next_pos[0]
                col = next_pos[1]
                while swap_dest > -1 and grid[swap_dest][col] not in '.#':
                    swap_dest -= 1
                if swap_dest == -1 or grid[swap_dest][col] == '#':
                    destination = robot
                else:
                    grid[swap_dest][col] = 'O'
                    grid[next_pos[0]][next_pos[1]] = '.'
                    destination = next_pos
        case '>':
            next_pos = (robot[0], robot[1] + 1)
            if grid[next_pos[0]][next_pos[1]] == '#':
                destination = robot
            elif grid[next_pos[0]][next_pos[1]] == '.':
                destination = next_pos
            else:
                row = grid[robot[0]]
                swap_dest = next_pos[1]
                while swap_dest < len(row) and row[swap_dest] not in '.#':
                    swap_dest += 1
                if swap_dest == len(row) or row[swap_dest] == '#':
                    destination = robot
                else:
                    row[swap_dest] = 'O'
                    row[next_pos[1]] = '.'
                    destination = next_pos
    
    return destination

def calculate_gps_score(grid):
    result = 0
    for i in range(len(grid)):
        row = grid[i]
        for j in range(len(row)):
            if grid[i][j] == 'O':
                result += (i * 100) + j
    return result

def get_solution(input_path):
    with open(input_path) as input_file:
        robot = None
        grid = []
        moves = ''
        reading_grid = True

        for l in input_file.readlines():
            if l.strip() == '':
                reading_grid = False
            elif reading_grid:
                row = list(l.strip())
                if '@' in row:
                    robot = (len(grid), row.index('@'))
                    row[row.index('@')] = '.'
                grid.append(row)
            else:
                moves += l.strip()

        for move in moves:
            robot = do_move(move, grid, robot)
            
    return calculate_gps_score(grid)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input_path", help="Input file path")
    args = parser.parse_args()
    print(get_solution(args.input_path))

    
