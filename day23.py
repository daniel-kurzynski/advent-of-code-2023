from aocd import get_data, submit
import re
from collections import deque

data = '''#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#'''

data = get_data(day=23, year=2023)

def parse_data(data):
    grid = [list(line) for line in data.split('\n')]
    return grid

def build_adjacent_graph(grid, igore_slopes=False):
    directions = {'^': (-1, 0), '>': (0, 1), 'v': (1, 0), '<': (0, -1)}
    max_rows, max_cols = len(grid), len(grid[0])
    graph = {}
    visited = set()

    def is_valid(x, y):
        return 0 <= x < max_rows and 0 <= y < max_cols and grid[x][y] != '#'

    def add_edge(node1, node2, path_length):
        if node1 not in graph:
            graph[node1] = {}
        if node2 not in graph:
            graph[node2] = {}
        graph[node1][node2] = path_length

    def get_direct_neighbors(previous, current):
        x,y = current
        neighbors = []
        local_directions = [directions[grid[x][y]]] if grid[x][y] in directions and not igore_slopes else directions.values()
        for dx, dy in local_directions:
            nx, ny = x + dx, y + dy
            if is_valid(nx, ny) and (nx, ny) != previous:
                neighbors.append((nx, ny))
        return neighbors

    def find_next_edge(previous, current, end_node):
        path_length = 1
        while True:
            x,y = current
            neighbours = get_direct_neighbors(previous, current)
            if len(neighbours) == 1:
                previous = (x, y)
                current = neighbours[0]
            else:
                if len(neighbours) == 0:
                    return (end_node if (x,y) == end_node else None), path_length
                else:
                    return (x, y), path_length
            path_length += 1

    # Find the start (top row) and end (bottom row) nodes
    start_node = next((i, j) for j in range(max_cols) for i in [0, max_rows - 1] if grid[i][j] == '.')
    graph[start_node] = {}
    end_node = next((i, j) for j in range(max_cols) for i in [max_rows - 1, 0] if grid[i][j] == '.' and (i, j) != start_node)
    graph[end_node] = {}

    queue = deque([start_node])

    while queue:
        current = queue.popleft()
        if current in visited:
            continue
        visited.add(current)
        for neighbor in get_direct_neighbors(None, current):
            edge, path_length = find_next_edge(current, neighbor, end_node)
            if edge is not None:
                add_edge(current, edge, path_length)
                queue.append(edge)

    return graph

def find_longest_hike(graph, start_node, end_node):
    def dfs(path, length):
        if path[-1] == end_node:
            return path, length
        max_path = []
        max_length = 0
        for neighbor, path_length in graph[path[-1]].items():
            if neighbor not in path:
                new_path, new_length = dfs(path + [neighbor], length + path_length)
                if new_length > max_length:
                    max_path = new_path
                    max_length = new_length

        return max_path, max_length

    longest_path, length = dfs([start_node], 0)
    return length

grid = parse_data(data)

max_rows, max_cols = len(grid), len(grid[0])
start_node = next((i, j) for j in range(max_cols) for i in [0, max_rows - 1] if grid[i][j] == '.')
end_node = next((i, j) for j in range(max_cols) for i in [max_rows - 1, 0] if grid[i][j] == '.' and (i, j) != start_node)


adjacency_graph = build_adjacent_graph(grid)
longest_path_length = find_longest_hike(adjacency_graph, start_node, end_node)
print(f"Part 1 - Longest Path Length: {longest_path_length}")

adjacency_graph = build_adjacent_graph(grid, igore_slopes=True)
longest_path_length = find_longest_hike(adjacency_graph, start_node, end_node)

print(f"Part 2 - Longest Path Length ignoring slopes: {longest_path_length}")