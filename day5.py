from aocd import get_data, submit
import re


# data = "seeds: 79 14 55 13\n\nseed-to-soil map:\n50 98 2\n52 50 48\n\nsoil-to-fertilizer map:\n0 15 37\n37 52 2\n39 0 15\n\nfertilizer-to-water map:\n49 53 8\n0 11 42\n42 0 7\n57 7 4\n\nwater-to-light map:\n88 18 7\n18 25 70\n\nlight-to-temperature map:\n45 77 23\n81 45 19\n68 64 13\n\ntemperature-to-humidity map:\n0 69 1\n1 0 69\n\nhumidity-to-location map:\n60 56 37\n56 93 4"
data = get_data(day=5, year=2023)


def parse_data(data):
    elements = data.split("\n\n")
    seeds = [int(seed) for seed in elements[0].split(":")[1].strip().split(" ") if seed != ""]

    seeds_ranges = []
    for index in range(len(seeds)//2):
        seeds_ranges.append((seeds[2*index], seeds[2*index+1]))

    mappings = []
    for element in elements[1:]:
        rules = []
        for row in element.split("\n")[1:]:
            rules.append([int(number) for number in row.strip().split(" ") if number != ""])
        mappings.append(rules)

    return (seeds, seeds_ranges, mappings)

seeds, seeds_ranges, mappings = parse_data(data)

def translate_for_single_seed(seed, mappings):
    current = seed
    for mapping in mappings:
        for (destination, source, length) in mapping:
            translation = destination - source
            if current >= source and current < source + length:
                current = current + translation
                break
    return current

print(f"Part 1: Minimal location: {min([translate_for_single_seed(seed, mappings) for seed in seeds])}")

def translate_for_range(seed_ranges, mappings):
    current_ranges = []
    current_ranges.extend(seed_ranges)
    next_ranges = []
    while len(current_ranges) > 0:
        (range_start, range_length) = current_ranges.pop()
        mapping = mappings[0]
        rule_matched = False
        for (destination_start, source_start, length) in mapping:
            translation = destination_start - source_start
            source_end = source_start + length
            range_end = range_start + range_length

            #range is not contained in mapping rule
            if range_end <= source_start or range_start >= source_end:
                continue

            # range is fully contained in mapping rule
            if range_start >= source_start and range_end <= source_end:
                next_ranges.append((range_start+translation, range_length))
                rule_matched = True
                break;

            #else break ranges
            if range_start < source_start:
                current_ranges.append((range_start, source_start-range_start))
                current_ranges.append((source_start, range_length-(source_start-range_start)))
                rule_matched = True
                break

            if range_end > source_end:
                current_ranges.append((range_start, source_end-range_start))
                current_ranges.append((source_end, range_end-source_end))
                rule_matched = True
                break

        if rule_matched == False:
            next_ranges.append((range_start, range_length))

    if len(mappings) <= 1:
        return next_ranges

    return translate_for_range(next_ranges, mappings[1:])


print(f"Part 2: Minimal location for ranges: {min([range_start for (range_start, range_length) in translate_for_range(seeds_ranges, mappings)])}")





