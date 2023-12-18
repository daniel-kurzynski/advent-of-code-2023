from aocd import get_data, submit
import numpy as np

# data = ".|...\\....\n|.-.\\.....\n.....|-...\n........|.\n..........\n.........\\\n..../.\\\\..\n.-.-/..|..\n.|....-|.\n..//.|....\n"
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

def simulate_beam(grid):
    # Stack of beams, each beam is represented as (x, y, dx, dy)
    stack = [(0, 0, 1, 0)]  # Start with the initial beam
    energized_tiles = set()
    visited = set()

    while stack:
        x, y, dx, dy = stack.pop()

        # Skip processing if the beam is out of bounds or already visited
        if not (0 <= y < len(grid) and 0 <= x < len(grid[0])) or (x, y, dx, dy) in visited:
            continue

        visited.add((x, y, dx, dy))
        energized_tiles.add((x, y))
        current = grid[y][x]

        if current == '.' or current == '-' and dy == 0 or current == '|' and dx == 0:
            stack.append((x + dx, y + dy, dx, dy))
        elif current == '/':
            # Reflect 90 degrees
            new_dx, new_dy = -dy, -dx
            stack.append((x + new_dx, y + new_dy, new_dx, new_dy))
        elif current == '\\':
            # Reflect 90 degrees in the other direction
            new_dx, new_dy = dy, dx
            stack.append((x + new_dx, y + new_dy, new_dx, new_dy))
        if current == '|' and abs(dx) == 1:  # Vertical beam
            stack.append((x, y + 1, 0, 1))  # Down
            stack.append((x, y - 1, 0, -1))  # Up
        elif current == '-' and abs(dy) == 1:  # Horizontal beam
            stack.append((x + 1, y, 1, 0))  # Right
            stack.append((x - 1, y, -1, 0))  # Left
    # visualize(grid, energized_tiles)
    return len(energized_tiles)


grid = parse_data(data)
result = simulate_beam(grid)

print(f"Part 1 - Energized Tiles: {result}")