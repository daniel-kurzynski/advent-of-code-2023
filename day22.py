from aocd import get_data, submit
import re
import numpy as np


# data = '1,0,1~1,2,1\n0,0,2~2,0,2\n0,2,3~2,2,3\n0,0,4~0,2,4\n2,0,5~2,2,5\n0,1,6~2,1,6\n1,1,8~1,1,9'
data = get_data(day=22, year=2023)

class Brick:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.supported_by = set()
        self.supporting = set()

    def __repr__(self):
        return f"Brick(start={self.start}, end={self.end})"

def parse_data(data):
    bricks = []
    for index, line in enumerate(data.split('\n')):
        start_end = line.split('~')
        start = tuple(map(int, start_end[0].split(',')))
        end = tuple(map(int, start_end[1].split(',')))

        # Ensure start has the lower z-coordinate
        if start[2] > end[2]:
            start, end = end, start

        bricks.append(Brick(start, end))

    # Sort bricks by the z-coordinate of their start point
    bricks.sort(key=lambda brick: brick.start[2])
    return bricks

def simulate_settling(bricks):
    max_x = max(brick.end[0] for brick in bricks) + 1
    max_y = max(brick.end[1] for brick in bricks) + 1

    heights = np.zeros((max_x, max_y), dtype=int)
    settled = np.full((max_x, max_y), None)

    for index, brick in enumerate(bricks):
        min_x, max_x = sorted([brick.start[0], brick.end[0]])
        min_y, max_y = sorted([brick.start[1], brick.end[1]])
        min_z, max_z = sorted([brick.start[2], brick.end[2]])

        current_height = heights[min_x:max_x+1, min_y:max_y+1].max()
        if current_height >= min_z:
            raise Exception(f"Brick {index} was not sorted correctly")

        where = np.argwhere(heights[min_x:max_x+1, min_y:max_y+1] == current_height)
        supporting_bricks = set(settled[x + min_x, y + min_y] for x, y in where if settled[x + min_x, y + min_y] is not None)

        brick.supported_by = supporting_bricks
        for supporting_brick_id in supporting_bricks:
            bricks[supporting_brick_id].supporting.add(index)


        brick_height = max_z - min_z + 1
        heights[min_x:max_x+1, min_y:max_y+1] = current_height + brick_height
        settled[min_x:max_x+1, min_y:max_y+1] = index

def count_safe_disintegrations(bricks):
    safe_count = 0

    for index, brick in enumerate(bricks):
        # Check if every brick that this brick supports has at least one other supporting brick
        can_disintegrate = True
        for supported_brick_id in brick.supporting:
            supported_brick = bricks[supported_brick_id]
            if len(supported_brick.supported_by - {index}) == 0:
                can_disintegrate = False
                break

        if can_disintegrate:
            safe_count += 1

    return safe_count


bricks = parse_data(data)
simulate_settling(bricks)
safe_disintegrations = count_safe_disintegrations(bricks)

print(f"Part 1 - Number of bricks that can be safely disintegrated: {safe_disintegrations}")

def count_falling_bricks(bricks):
    falling_bricks_count = 0

    for index, brick in reversed(list(enumerate(bricks))):
        falling_bricks = set()
        queue = [index]
        while queue:
            brick_id = queue.pop()
            brick = bricks[brick_id]

            for supporting_brick_id in brick.supporting:
                supporting_brick = bricks[supporting_brick_id]
                if len(supporting_brick.supported_by - {index} - falling_bricks) == 0:
                    falling_bricks.add(supporting_brick_id)
                    queue.append(supporting_brick_id)

        falling_bricks_count += len(falling_bricks)

    return falling_bricks_count

print("Part 2 - Number of bricks that will fall: ", count_falling_bricks(bricks))