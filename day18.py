from aocd import get_data, submit
import re

# data = 'R 6 (#70c710)\nD 5 (#0dc571)\nL 2 (#5713f0)\nD 2 (#d2c081)\nR 2 (#59c680)\nD 2 (#411b91)\nL 5 (#8ceee2)\nU 2 (#caa173)\nL 1 (#1b58a2)\nU 2 (#caa171)\nR 2 (#7807d2)\nU 3 (#a77fa3)\nL 2 (#015232)\nU 2 (#7a21e3)'
data = get_data(day=18, year=2023)

def parse_data(data):
    instructions = []
    for line in data.split('\n'):
        direction, distance, _ = line.split()
        instructions.append((direction, int(distance)))
    return instructions

def calculate_lava_capacity(instructions):
    x, y = 0, 0
    path = set()

    for direction, distance in instructions:
        dx, dy = 0, 0
        if direction == 'R':
            dx = 1
        elif direction == 'L':
            dx = -1
        elif direction == 'U':
            dy = -1
        elif direction == 'D':
            dy = 1

        for _ in range(distance):
            x += dx
            y += dy
            path.add((x, y))

    min_x = min(x for x, _ in path)
    max_x = max(x for x, _ in path)
    min_y = min(y for _, y in path)
    max_y = max(y for _, y in path)

    visited = set()
    stack = [(min_x - 1, min_y - 1)]

    while stack:
        cx, cy = stack.pop()
        if (cx, cy) in visited or (cx, cy) in path:
            continue
        visited.add((cx, cy))

        for nx, ny in [(cx - 1, cy), (cx + 1, cy), (cx, cy - 1), (cx, cy + 1)]:
            if min_x - 1 <= nx <= max_x + 1 and min_y - 1 <= ny <= max_y + 1:
                stack.append((nx, ny))

    total_area = (max_x - min_x + 3) * (max_y - min_y + 3)
    lava_capacity = total_area - len(visited)

    return lava_capacity

instructions = parse_data(data)
lava_capacity = calculate_lava_capacity(instructions)
print(f"Lavaduct Lagoon Capacity: {lava_capacity}")
