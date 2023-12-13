import numpy as np
from aocd import get_data, submit

# data = '#.##..##.\n..#.##.#.\n##......#\n##......#\n..#.##.#.\n..##..##.\n#.#.##.#.\n\n#...##..#\n#....#..#\n..##..###\n#####.##.\n#####.##.\n..##..###\n#....#..#'  # Example data
data = get_data(day=13, year=2023)

def parse_data(data):
    patterns = data.strip().split('\n\n')
    return [np.array([list(row) for row in pattern.split('\n')]) for pattern in patterns]

def find_reflection_line(pattern, smudge=False):
    def check_reflection(arr, smudge):
        rows, cols = arr.shape
        for i in range(0, rows-1):
            if np.array_equal(arr[i], arr[i+1]) or (smudge and np.sum(arr[i] != arr[i+1]) == 1):
                reflection_width = min(i+1, rows-i-1)
                matching_area = arr[i+1-reflection_width:i+1]
                reflected_area = np.flipud(arr[i+1:i+1+reflection_width])

                if (not smudge and np.array_equal(matching_area, reflected_area)) or (smudge and np.sum(matching_area != reflected_area) == 1):
                    return i
        return None

    reflection_row = check_reflection(pattern, smudge)
    if reflection_row is not None:
        return 'horizontal', reflection_row

    rotated_pattern = np.rot90(pattern, axes=[1,0])
    reflection_col = check_reflection(rotated_pattern, smudge)
    if reflection_col is not None:
        return 'vertical', reflection_col

    return None, None

def calculate_summary(patterns, smudge=False):
    total = 0
    for pattern in patterns:
        line_type, position = find_reflection_line(pattern, smudge)
        if line_type == 'horizontal':
            total += 100 * (position + 1)
        elif line_type == 'vertical':
            total += position + 1
    return total

# Part 1
patterns = parse_data(data)
summary = calculate_summary(patterns)
print(f"Part 1 - Summary: {summary}")

# Part 2
new_summary = calculate_summary(patterns, smudge=True)
print(f"Part 2 - New Summary: {new_summary}")
