from aocd import get_data
import functools
from functools import cache

data = get_data(day=12, year=2023)
# data = "???.### 1,1,3\n.??..??...?##. 1,1,3\n?#?#?#?#?#?#?#? 1,3,1,6\n????.#...#... 4,1,1\n????.######..#####. 1,6,5\n?###???????? 3,2,1"

@cache
def count_arrangements(spring_row, group_sizes, position, current_group_size, current_groups):
    if position == len(spring_row):
        return 1 if current_groups == len(group_sizes) else 0

    elements = ["#", "."] if spring_row[position] == '?' else [spring_row[position]]

    arrangements = 0
    for element in elements:
        if element == "#":
            #Too many groups or too many elements in group
            if current_groups + 1 > len(group_sizes) or current_group_size + 1 > group_sizes[current_groups]:
                continue
            arrangements += count_arrangements(spring_row, group_sizes, position + 1, current_group_size + 1, current_groups)
        else:
            #Currently not in a group
            if current_group_size == 0:
                arrangements += count_arrangements(spring_row, group_sizes, position + 1, 0, current_groups)
            #Currently in a group -> found end of group
            else:
                #already too many groups
                if current_groups + 1 > len(group_sizes):
                    continue
                #Group is too big or too small
                if current_group_size != group_sizes[current_groups]:
                    continue
                arrangements += count_arrangements(spring_row, group_sizes, position + 1, 0, current_groups + 1)

    return arrangements

def unfold_row(spring_row, group_sizes):
    unfolded_row = ('?'.join([spring_row] * 5))
    unfolded_group_sizes = group_sizes * 5
    return unfolded_row, unfolded_group_sizes


def solve(data, unfold=False):
    total_arrangements = 0
    lines = data.splitlines()
    for index, line in enumerate(lines):
        spring_row, group_sizes_str = line.split(' ')
        group_sizes = tuple(map(int, group_sizes_str.split(',')))

        if unfold:
            spring_row, group_sizes = unfold_row(spring_row, group_sizes)

        arrangements = count_arrangements(spring_row + ".", group_sizes, 0, 0, 0)
        total_arrangements += arrangements

    return total_arrangements


print(f"Part 1 - Total Arrangements: {solve(data, False)}")

print(f"Part 2 - Total Arrangements: {solve(data, True)}")