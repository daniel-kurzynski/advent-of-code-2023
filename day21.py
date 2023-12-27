from aocd import get_data, submit
import numpy as np


# data = '...........\n.....###.#.\n.###.##..#.\n..#.#...#..\n....#.#....\n.##..S####.\n.##..#...#.\n.......##..\n.##.#.####.\n.##..##.##.\n...........'
data = get_data(day=21, year=2023)

def parse_data(data):
    grid = data.split('\n')
    start = None
    for i, row in enumerate(grid):
        if 'S' in row:
            start = (i, row.index('S'))
            break
    return grid, start

def print_grid(grid, reachable_plots):
    for i, row in enumerate(grid):
        for j, cell in enumerate(row):
            if (i, j) in reachable_plots:
                print('0', end='')
            else:
                print(cell, end='')
        print()

def simulate_steps(grid, start, steps, infinite=False, trace_config=None):
    grid_size = len(grid)
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    current = set([start])
    grid_height = len(grid)
    grid_width = len(grid[0])
    visited = [set(),set()]
    trace = [ ]

    for i in range(steps):
        next = set()
        for position in current:
            visited[i % 2].add(position)
            for dx, dy in directions:
                new_x, new_y = position[0] + dx, position[1] + dy

                # For infinite grid, wrap around using modulo
                wrapped_x, wrapped_y = (new_x % grid_height, new_y % grid_width) if infinite else (new_x, new_y)

                # Check for valid position and garden plot
                if 0 <= wrapped_x < grid_height and 0 <= wrapped_y < grid_width:
                    if grid[wrapped_x][wrapped_y] in ['.', 'S']:
                        if (new_x, new_y) not in visited[(i-1) % 2]:
                            next.add((new_x, new_y))

        current = next
        if trace_config and (i + 1) % trace_config[0] == trace_config[1]:
            trace.append(((i+1) // trace_config[0], len(current.union(visited[(i + 1) % 2]))))

    return trace, len(current.union(visited[(steps) % 2]))

grid, start = parse_data(data)
_, result = simulate_steps(grid, start, 64)
print(f"Part 1 - Number of reachable plots: {result}")

steps = 26501365
grid_size = len(grid)
offset = steps % grid_size

trace, result = simulate_steps(grid, start, 3 * grid_size, infinite=True, trace_config=(grid_size, offset))

func = np.poly1d(np.polyfit([x[0] for x in trace], [x[1] for x in trace], 2))
print(f"Part 2 - Number of reachable plots: {round(func(steps//grid_size))}")