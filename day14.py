from aocd import get_data, submit
import numpy as np

# data = 'O....#....\nO.OO#....#\n.....##...\nOO.#O....O\n.O.....O#.\nO.#..O.#.#\n..O..#O..O\n.......O..\n#....###..\n#OO..#....'
data = get_data(day=14, year=2023)

def parse_data(data):
    lines = data.splitlines()
    grid_size = len(lines[0]) + 2
    padded_lines = ['#' * grid_size] + ['#' + line + '#' for line in lines] + ['#' * grid_size]
    return np.array([list(line) for line in padded_lines])

def tilt_north(grid):
    tilted_grid = grid.copy()
    for col in range(tilted_grid.shape[1]):
        column = tilted_grid[:, col]
        cube_indices = [i for i, cell in enumerate(column) if cell == '#']
        for i in range(len(cube_indices) - 1):
            num_round_rocks = list(column[cube_indices[i]:cube_indices[i + 1]]).count('O')
            tilted_grid[cube_indices[i] + 1:cube_indices[i] + 1 + num_round_rocks, col] = 'O'
            tilted_grid[cube_indices[i] + 1 + num_round_rocks:cube_indices[i + 1], col] = '.'
    return tilted_grid

def calculate_load(grid):
    num_rows = grid.shape[0]
    rows, _ = np.where(grid == 'O')
    return sum(num_rows - 1 - row for row in rows)

grid = parse_data(data)
tilted_grid = tilt_north(grid)
total_load = calculate_load(tilted_grid)

print(f"Part 1 - Total Load: {total_load}")

def simulate_cycles(grid, num_cycles):
    cycle_hashes = {}
    cycle = 0
    while cycle < num_cycles:
        grid_hash = hash(grid.tobytes())
        if grid_hash in cycle_hashes:
            cycle_diff = cycle - cycle_hashes[grid_hash]
            remaining_cycles = num_cycles - cycle
            skip_cycles = (remaining_cycles // cycle_diff) * cycle_diff
            cycle += skip_cycles
            if cycle >= num_cycles:
                break
        else:
            cycle_hashes[grid_hash] = cycle

        for i in range(4):
            grid = tilt_north(grid)
            grid = np.rot90(grid, axes=[1,0])  # Rotate for next tilt direction

        cycle += 1

    return grid

cycles = 1000000000
spun_grid = simulate_cycles(grid, cycles)
total_load = calculate_load(spun_grid)
print(f"Part 2 - Total Load after {cycles} Cycles: {total_load}")