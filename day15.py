from aocd import get_data, submit
import re

data = get_data(day=15, year=2023)
# data = 'rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7'  # Example data

def hash_algorithm(string):
    current_value = 0
    for char in string:
        ascii_code = ord(char)
        current_value = (current_value + ascii_code) * 17 % 256
    return current_value

def parse_data(data):
    return data.split(',')

parsed_data = parse_data(data)
sum_of_hashes = sum(hash_algorithm(step) for step in parsed_data)

print(f"Part 1 - Sum of HASH results: {sum_of_hashes}")

def process_data(data):
    hashmap = [{} for i in range(256)]
    for operation in data:
        if "-" in operation:
            label = operation.split("-")[0]
            hashmap[hash_algorithm(label)].pop(label, None)
        else:
            label = operation.split("=")[0]
            focal_length = int(operation.split("=")[1])
            hashmap[hash_algorithm(label)][label] = focal_length

    return hashmap

def calulate_box_power(box, box_index):
    total_power = 0
    for (slot_index, (_, focal_length)) in enumerate(box.items(), start=1):
        total_power += (box_index+1) * slot_index * focal_length
    return total_power

print(f"Part 2 - Processed data: {sum(calulate_box_power(box, box_index) for (box_index, box) in enumerate(process_data(parsed_data)))}")


