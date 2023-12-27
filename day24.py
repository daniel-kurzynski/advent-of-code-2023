from aocd import get_data, submit
from sympy import var, Eq, solve
import re

data = '''\n19, 13, 30 @ -2,  1, -2\n18, 19, 22 @ -1, -1, -2\n20, 25, 34 @ -2, -2, -4\n12, 31, 28 @ -1, -2, -1\n20, 19, 15 @  1, -5, -3\n'''
test_area = (7, 27)

data = get_data(day=24, year=2023)
test_area = (200000000000000, 400000000000000)

def parse_data(data):
    hailstones = []
    for line in data.strip().split('\n'):
        position, velocity = line.split('@')
        px, py, pz = map(int, position.split(','))
        vx, vy, vz = map(int, velocity.split(','))
        hailstones.append(((px, py, pz), (vx, vy, vz)))
    return hailstones


def check_path_intersection(hailstone1, hailstone2, test_area):
    (px1, py1, _), (vx1, vy1, _) = hailstone1
    (px2, py2, _), (vx2, vy2, _) = hailstone2

    # x = px1 + vx1 * t1 => t1 = (x - px1) / vx1
    # y = py1 + vy1 * t1 => t1 = (y - py1) / vy1
    # (x - px1) / vx1 = (y - py1) / vy1
    # x * vy1 - px1 * vy1 = y * vx1 - py1 * vx1
    # y = (x * vy1 - px1 * vy1 + py1 * vx1) / vx1
    # (x * vy1 - px1 * vy1 + py1 * vx1) / vx1 = (x * vy2 - px2 * vy2 + py2 * vx2) / vx2
    # x * vy1 * vx2 - px1 * vy1 * vx2 + py1 * vx1 * vx2 = x * vy2 * vx1 - px2 * vy2 * vx1 + py2 * vx2 * vx1
    # x * (vy1 * vx2 - vy2 * vx1) = px1 * vy1 * vx2 - py1 * vx1 * vx2 - px2 * vy2 * vx1 + py2 * vx2 * vx1
    # x = (px1 * vy1 * vx2 - py1 * vx1 * vx2 - px2 * vy2 * vx1 + py2 * vx2 * vx1) / (vy1 * vx2 - vy2 * vx1)

    if vx1 * vy2 == vx2 * vy1:
        return False

    x = (px1 * vy1 * vx2 - py1 * vx1 * vx2 - px2 * vy2 * vx1 + py2 * vx2 * vx1) / (vy1 * vx2 - vy2 * vx1)
    y = (x * vy1 - px1 * vy1 + py1 * vx1) / vx1

    t1 = (x - px1) / vx1
    t2 = (x - px2) / vx2

    is_in_future = t1 > 0 and t2 > 0
    is_in_test_area = test_area[0] <= x <= test_area[1] and test_area[0] <= y <= test_area[1]

    return is_in_future and is_in_test_area


def calculate_intersections(hailstones, test_area):
    intersections = 0
    for i in range(len(hailstones)):
        for j in range(i+1, len(hailstones)):
            if check_path_intersection(hailstones[i], hailstones[j], test_area):
                intersections += 1
    return intersections

hailstones = parse_data(data)
intersections = calculate_intersections(hailstones, test_area)

print(f"Part 1 - Number of intersections within the test area: {intersections}")

def calc_throwing(hailstones):
    px0, py0, pz0 = var("px0,py0,pz0")
    vx0, vy0, vz0 = var("vx0,vy0,vz0")

    equations = []
    for index, stone in enumerate(hailstones[:5]):
        t = var("t"+str(index))
        (px, py, pz), (vx, vy, vz) = stone
        equations.extend([
            Eq(px + vx * t, px0 + vx0 * t),
            Eq(py + vy * t, py0 + vy0 * t),
            Eq(pz + vz * t, pz0 + vz0 * t)
        ])

    solutions = solve(equations, dict=True)

    if len(solutions) == 0:
        return None, None, None, None, None, None
    solution = solutions[0]
    return (solution[px0], solution[py0], solution[pz0], solution[vx0], solution[vy0], solution[vz0])

ax, ay, az, bx, by, bz = calc_throwing(hailstones)

print(f"Part 2 - Initial position {(ax, ay, az)} with velocity {(bx, by, bz)} results in {sum([ax, ay, az])}")