from aocd import get_data, submit
import heapq

# data = '2413432311323\n3215453535623\n3255245654254\n3446585845452\n4546657867536\n1438598798454\n4457876987766\n3637877979653\n4654967986887\n4564679986453\n1224686865563\n2546548887735\n4322674655533'
data = get_data(day=17, year=2023)

def parse_data(data):
    return [[int(x) for x in line] for line in data.split('\n')]

def find_min_heat_loss(grid, min_steps, max_steps):
    def neighbors(pos, direction, steps):
        x, y = pos
        directions = {'U': (-1, 0), 'D': (1, 0), 'L': (0, -1), 'R': (0, 1)}
        turns = {'U': {'L': 'L', 'R': 'R' }, 'D': {'L': 'R', 'R': 'L'}, 'L': {'L': 'D', 'R': 'U'}, 'R': {'L': 'U', 'R': 'D'}}
        result = []

        # Continue in the same direction if within step limits
        if steps < max_steps:
            dx, dy = directions[direction]
            nx, ny = x + dx, y + dy
            if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]):
                result.append((nx, ny, direction, steps + 1))

        # Turn left and right if steps are equal to or exceed min_steps
        if steps >= min_steps:
            for turn in ['L', 'R']:
                nd = turns[direction][turn]
                dx, dy = directions[nd]
                nx, ny = x + dx, y + dy
                if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]):
                    result.append((nx, ny, nd, 1))

        return result

    heap = [(0, (0, 0, 'D', 0) ),(0, (0, 0, 'R', 0))]  # Heat loss, position
    visited = set()

    while heap:
        heat_loss, (x, y, direction, steps) = heapq.heappop(heap)
        if (x, y) == (len(grid)-1, len(grid[0])-1):
            return heat_loss
        if (x, y, direction, steps) in visited:
            continue
        visited.add((x, y, direction, steps))

        for nx, ny, nd, next_steps in neighbors((x, y), direction, steps):
            if (nx, ny, nd, next_steps) not in visited:
                heapq.heappush(heap, (heat_loss + grid[nx][ny], (nx, ny, nd, next_steps)))

    return float('inf')

grid = parse_data(data)

print(f"Part 1 - Least Heat Loss for Normal Crucible: {find_min_heat_loss(grid, 1, 3)}")
print(f"Part 2 - Least Heat Loss for Ultra Crucible: {find_min_heat_loss(grid, 4, 10)}")
