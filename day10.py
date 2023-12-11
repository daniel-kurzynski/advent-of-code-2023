from aocd import get_data, submit

# data = '..F7.\n.FJ|.\nSJ.L7\n|F--J\nLJ...'
data = get_data(day=10, year=2023)


directions = {'N': (-1, 0), 'E': (0, 1), 'S': (1, 0), 'W': (0, -1)}
opposite = {'N': 'S', 'E': 'W', 'S': 'N', 'W': 'E'}

def parse_data(data):
    return [list(line) for line in data.split('\n')]

def get_connected_directions(pipe):
    pipe_directions = {
        '|': ['N', 'S'],
        '-': ['E', 'W'],
        'L': ['N', 'E'],
        'J': ['N', 'W'],
        '7': ['S', 'W'],
        'F': ['S', 'E']
    }
    return pipe_directions.get(pipe, [])

def next_position(grid, x, y, prev_direction):
    for direction in get_connected_directions(grid[x][y]):
        if direction != opposite.get(prev_direction, ''):
            dx, dy = directions[direction]
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]):
                return (nx, ny, direction)
    return None

def get_starting_position(grid):
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if cell == 'S':
                return i, j
    return None, None

def find_loop(grid):
    start_x, start_y = get_starting_position(grid)
    max_distance = 0
    loop = set()

    for direction in ['N', 'E', 'S', 'W']:
        x = start_x + directions[direction][0]
        y = start_y + directions[direction][1]

        path = {(start_x, start_y), (x, y)}

        if not(0 <= x < len(grid) and 0 <= y < len(grid[0])):
            continue

        steps = 1

        while True:
            next = next_position(grid, x, y, direction)

            if not next:
                break
            (x, y, direction) = next
            path.add((x, y))

            steps += 1

            if (x, y) == (start_x, start_y):
                if steps // 2 > max_distance:
                    max_distance = steps // 2
                    loop = path
                break

    return max_distance, loop

grid = parse_data(data)
max_distance, loop = find_loop(grid)

print(f"Part 1 - Farthest Point Distance: {max_distance}")

def find_enclosed_titles(grid, loop):
    num_rows = len(grid)
    num_cols = len(grid[0])

    inside_loop = 0
    for x, row in enumerate(grid):
        for y, cell in enumerate(row):
            if (x, y) in loop:
                continue;

            cross_loop = 0
            dx,dy = x,y
            while dx < num_rows and dy < num_cols:
                pipe = grid[dx][dy]
                if (dx, dy) in loop and pipe in ['|', '-', 'J', 'F']:
                    cross_loop += 1
                dx += 1
                dy += 1

            if cross_loop % 2 == 1:
                inside_loop += 1




    return inside_loop

print(f"Part 2 - Enclosed Tiles: {find_enclosed_titles(grid, loop)}")
