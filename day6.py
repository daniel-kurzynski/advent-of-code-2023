import math

from aocd import get_data, submit
import re
import numpy as np

# data = 'Time: 7 15 30\nDistance: 9 40 200\n'
data = get_data(day=6, year=2023)

def parse_data(data, ignore_spaces=False):
    time_pattern = r"Time: (.+)"
    distance_pattern = r"Distance: (.+)"
    if ignore_spaces:
        time = int(re.findall(time_pattern, data)[0].replace(" ", ""))
        distance = int(re.findall(distance_pattern, data)[0].replace(" ", ""))
        return [(time, distance)]
    else:
        times = list(map(int, re.findall(time_pattern, data)[0].split()))
        distances = list(map(int, re.findall(distance_pattern, data)[0].split()))
        return list(zip(times, distances))

def calculate_ways_to_win(races):
    total_ways = []
    for time, record in races:
        ways = 0
        p = -time
        q = record
        discriminant = (p / 2) ** 2 - q

        if discriminant >= 0:
            start = -p / 2 - math.sqrt(discriminant)
            end = -p / 2 + math.sqrt(discriminant)

            start = math.ceil(start)+1 if math.ceil(start) == start else math.ceil(start)
            end = math.floor(end)-1 if math.floor(end) == end else math.floor(end)

            ways = end - start + 1
        total_ways.append(ways)
    return total_ways

races = parse_data(data)
ways_to_win = calculate_ways_to_win(races)
print(f"Part 1 - Product of total ways to win: {np.prod(ways_to_win)}")

races = parse_data(data, ignore_spaces=True)
ways_to_win = calculate_ways_to_win(races)
print(f"Part 2 - Total ways to win: {ways_to_win[0]}")
