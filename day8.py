from aocd import get_data
from math import lcm
import re

data = get_data(day=8, year=2023)
# data = 'LLR\n\nAAA = (BBB, BBB)\nBBB = (AAA, ZZZ)\nZZZ = (ZZZ, ZZZ)'
def parse_data(data):
    instructions, mappings = data.split('\n\n')
    node_map = {
        match.group(1): (match.group(2), match.group(3))
        for match in re.finditer(r'(\w+) = \((\w+), (\w+)\)', mappings)
    }
    return instructions, node_map

def execute_instructions(start_node, mappings, instructions):
    current_node = start_node
    for instruction in instructions:
        direction = 0 if instruction == 'L' else 1
        current_node = mappings[current_node][direction]
    return current_node

def execute_steps(start_node, extended_mapping, steps):
    current_node = start_node
    for step in range(steps):
        current_node = extended_mapping[current_node]
    return current_node

def build_extended_mapping(mappings, instructions):
    extended_map = {}
    for start_node in mappings.keys():
        end_node = execute_instructions(start_node, mappings, instructions)
        extended_map[start_node] = end_node
    return extended_map

def navigate(start_nodes, goal_nodes, extended_map, instruction_length):
    current_nodes = start_nodes
    iteration_count = 0

    found_goals = [None] * len(goal_nodes)

    while True:
        current_nodes = [extended_map[node] for node in current_nodes]
        iteration_count += 1

        if all(node in goal_nodes for node in current_nodes):
            break

        for index, node in enumerate(current_nodes):
            if node in goal_nodes and not found_goals[index] and execute_steps(node, extended_map, iteration_count) == node:
                found_goals[index] = iteration_count

        if(all(found_goals)):
            iteration_count = lcm(*found_goals)
            break

    return iteration_count * instruction_length

# For Part One
instructions, node_map = parse_data(data)
extended_map = build_extended_mapping(node_map, instructions)
steps_part_one = navigate(['AAA'], ['ZZZ'], extended_map, len(instructions))
print(f"Part 1 - Steps required to reach ZZZ: {steps_part_one}")

# For Part Two
start_nodes = [node for node in node_map if node.endswith('A')]
goal_nodes = [node for node in node_map if node.endswith('Z')]
steps_part_two = navigate(start_nodes, goal_nodes, extended_map, len(instructions))
print(f"Part 2 - Steps required to reach all Z-nodes: {steps_part_two}")
