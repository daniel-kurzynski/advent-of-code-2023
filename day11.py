import numpy as np
from aocd import get_data
import itertools

data = get_data(day=11, year=2023)
# data = "...#......\n.......#..\n#.........\n..........\n......#...\n.#........\n.........#\n..........\n.......#..\n#...#....."

def parse_data(data):
    return np.array([list(line) for line in data.splitlines()])

def mark_empty_spaces(array):
    marked_array = np.array(array, copy=True)

    # Mark empty columns
    for col in range(array.shape[1]):
        if all(array[:, col] == '.'):
            marked_array[:, col] = 'E'

    # Mark empty rows
    for row in range(array.shape[0]):
        if all(array[row, :] == '.'):
            marked_array[row, :] = 'E'

    return marked_array

def identify_galaxies(marked_data):
    galaxy_positions = []
    for row in range(marked_data.shape[0]):
        for col in range(marked_data.shape[1]):
            if marked_data[row, col] != '.' and marked_data[row, col] != 'E':
                galaxy_positions.append((row, col))
    return galaxy_positions

def find_shortest_path(marked_data, start, end, e_value):
    row_start, row_end = sorted([start[0], end[0]])
    col_start, col_end = sorted([start[1], end[1]])

    manhattan_distance = abs(start[0] - end[0]) + abs(start[1] - end[1])
    e_count = np.count_nonzero(marked_data[row_start:row_end+1, col_start] == 'E') + np.count_nonzero(marked_data[row_end, col_start:col_end+1] == 'E')
    return manhattan_distance + e_count * (e_value - 1)

grid = parse_data(data)
marked_data = mark_empty_spaces(grid)
galaxies = identify_galaxies(grid)

def solve(galaxies, marked_data, e_value):
    total_length = 0
    for galaxy1, galaxy2 in itertools.combinations(galaxies, 2):
        path_length = find_shortest_path(marked_data, galaxy1, galaxy2, e_value)
        total_length += path_length

    return total_length


print(f"Part 1 - Total length of all shortest paths: {solve(galaxies, marked_data, 2)}")
print(f"Part 2 - Total length of all shortest paths: {solve(galaxies, marked_data, 1000000)}")
