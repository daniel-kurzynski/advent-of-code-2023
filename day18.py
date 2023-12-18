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
    length = 0
    vertices = [(0, 0)]
    x, y = 0, 0

    for direction, distance in instructions:
        length += distance
        if direction == 'R':
            x += distance
        elif direction == 'L':
            x -= distance
        elif direction == 'U':
            y += distance
        elif direction == 'D':
            y -= distance
        vertices.append((x, y))

    # Apply the Shoelace formula
    area = 0
    for i in range(len(vertices)-1):
        x1, y1 = vertices[i]
        x2, y2 = vertices[i + 1]
        area += (y1+y2) * (x1 - x2)
    area = abs(area) // 2 + length // 2 + 1

    return area

instructions = parse_data(data)
lava_capacity = calculate_lava_capacity(instructions)
print(f"Part 1 - Lavaduct Lagoon Capacity: {lava_capacity}")

def parse_data_hex(data):
    instructions = []
    direction_map = {0: 'R', 1: 'D', 2: 'L', 3: 'U'}
    for line in data.split('\n'):
        _, hex_code = line.rsplit(' ', 1)
        distance = int(hex_code[2:7], 16)
        direction = direction_map[int(hex_code[7], 16)]
        instructions.append((direction, distance))
    return instructions

instructions_hex = parse_data_hex(data)
lava_capacity = calculate_lava_capacity(instructions_hex)
print(f"Part 2 - Lavaduct Lagoon Capacity from Hex: {lava_capacity}")