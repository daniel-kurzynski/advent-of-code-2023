from aocd import get_data, submit
import numpy as np

# data = ".|...\\....\n|.-.\\.....\n.....|-...\n........|.\n..........\n.........\\\n..../.\\\\..\n.-.-/..|..\n.|....-|.\\\n..//.|...."
data = get_data(day=16, year=2023)

def parse_data(data):
    grid = [list(line) for line in data.split('\n') if line]
    return grid

def visualize(grid, energized_tiles):
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if (x, y) in energized_tiles:
                print('#', end='')
            else:
                print('.', end='')
        print()
    print()

def simulate_beam(grid, start_x=0, start_y=0, initial_dx=1, initial_dy=0):
    stack = [(start_x, start_y, initial_dx, initial_dy)]
    energized_tiles = set()
    visited = set()

    while stack:
        x, y, dx, dy = stack.pop()
        if not (0 <= y < len(grid) and 0 <= x < len(grid[0])) or (x, y, dx, dy) in visited:
            continue

        visited.add((x, y, dx, dy))
        energized_tiles.add((x, y))
        current = grid[y][x]

        if current == '.' or current == '-' and dy == 0 or current == '|' and dx == 0:
            stack.append((x + dx, y + dy, dx, dy))
        elif current == '/':
            new_dx, new_dy = -dy, -dx
            stack.append((x + new_dx, y + new_dy, new_dx, new_dy))
        elif current == '\\':
            new_dx, new_dy = dy, dx
            stack.append((x + new_dx, y + new_dy, new_dx, new_dy))
        if current == '|' and abs(dx) == 1:
            stack.append((x, y + 1, 0, 1))
            stack.append((x, y - 1, 0, -1))
        elif current == '-' and abs(dy) == 1:
            stack.append((x + 1, y, 1, 0))
            stack.append((x - 1, y, -1, 0))

    return len(energized_tiles)

def find_best_starting_position(grid):
    max_energized = 0

    for x in range(len(grid[0])):
        max_energized = max(max_energized, simulate_beam(grid, x, 0, 0, 1))  # Top row, moving down
        max_energized = max(max_energized, simulate_beam(grid, x, len(grid)-1, 0, -1))  # Bottom row, moving up

    for y in range(len(grid)):
        max_energized = max(max_energized, simulate_beam(grid, 0, y, 1, 0))  # Left column, moving right
        max_energized = max(max_energized, simulate_beam(grid, len(grid[0])-1, y, -1, 0))  # Right column, moving left

    return max_energized

grid = parse_data(data)
part1_result = simulate_beam(grid)
print(f"Part 1 - Energized Tiles: {part1_result}")

part2_result = find_best_starting_position(grid)
print(f"Part 2 - Maximum Energized Tiles: {part2_result}")
