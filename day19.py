from aocd import get_data, submit
from collections import deque

import re

# data = 'px{a<2006:qkq,m>2090:A,rfg}\npv{a>1716:R,A}\nlnx{m>1548:A,A}\nrfg{s<537:gd,x>2440:R,A}\nqs{s>3448:A,lnx}\nqkq{x<1416:A,crn}\ncrn{x>2662:A,R}\nin{s<1351:px,qqz}\nqqz{s>2770:qs,m<1801:hdj,R}\ngd{a>3333:R,R}\nhdj{m>838:A,pv}\n\n{x=787,m=2655,a=1222,s=2876}\n{x=1679,m=44,a=2067,s=496}\n{x=2036,m=264,a=79,s=2244}\n{x=2461,m=1339,a=466,s=291}\n{x=2127,m=1623,a=2188,s=1013}'
data = get_data(day=19, year=2023)

def parse_data(data):
    workflows_section, parts_section = data.split("\n\n")

    workflow_pattern = re.compile(r'(\w+)\{(.+?)\}')
    rule_pattern = re.compile(r'(\w+)([<>]=?)(\d+):(\w+|R|A)')
    workflows = {}

    for line in workflows_section.split('\n'):
        name, rules_str = workflow_pattern.match(line).groups()
        rules_raw = rules_str.split(',')

        rules = []
        for r in rules_raw:
            if ":" in r:
                attribute, operator, value, outcome = rule_pattern.match(r).groups()
                rules.append((True, attribute, operator, int(value), outcome))
            else:
                rules.append((False, None, None, None, r))

        workflows[name] = rules

    part_pattern = re.compile(r'(\w+)=(\d+)')
    parts = []
    for line in parts_section.split('\n'):
        if line:
            part_dict = dict(part_pattern.findall(line.strip("{}")))
            parts.append({k: int(v) for k, v in part_dict.items()})

    return workflows, parts

workflows, parts = parse_data(data)

def apply_rules(part, rules):
    rule_code = ""

    for r in rules:
        if r[0]:
            _, attribute, operator, value, outcome = r
            rule_code += f"'{outcome}' if part['{attribute}'] {operator} {value} else "
        else:
            _, _, _, _, outcome = r
            rule_code += f"'{outcome}'"

    return eval(rule_code)

def process_part(part, workflows):
    next = "in"
    while next != 'A' and next != 'R':
        next = apply_rules(part, workflows[next])
    return next


workflows, parts = parse_data(data)
sum_ratings = sum(sum(part.values()) for part in parts if process_part(part, workflows) == 'A')
print(f"Part 1 - Sum of Ratings for Accepted Parts: {sum_ratings}")


def split_range(part_range, rule):
    conditional, attribute, operator, value, outcome = rule

    if conditional:
        start, end = part_range[attribute]
        if operator == '<':
            if end < value:
                return part_range, None, outcome  # Entire range matches
            elif start >= value:
                return None, part_range, outcome  # Entire range does not match
            else:
                return {**part_range, attribute: (start, value - 1)}, {**part_range, attribute: (value, end)}, outcome
        elif operator == '>':
            if start > value:
                return part_range, None, outcome  # Entire range matches
            elif end <= value:
                return None, part_range, outcome  # Entire range does not match
            else:
                return {**part_range, attribute: (value + 1, end)}, {**part_range, attribute: (start, value)}, outcome
    else:
        return part_range, None, outcome # Entire range matches

def process_ranges(workflows):
    queue = deque([({'x': (1, 4000), 'm': (1, 4000), 'a': (1, 4000), 's': (1, 4000)}, 'in')])
    accepted_ranges = []

    while queue:
        part_range, current_workflow = queue.popleft()
        for rule in workflows[current_workflow]:
            part_match, part_range_non_match, outcome = split_range(part_range, rule)

            if part_match and outcome not in ['A', 'R']:
                queue.append((part_match, outcome))
            elif part_match and outcome == 'A':
                accepted_ranges.append(part_match)

            part_range = part_range_non_match

    total_combinations = sum((r['x'][1] - r['x'][0] + 1) * (r['m'][1] - r['m'][0] + 1) *
                             (r['a'][1] - r['a'][0] + 1) * (r['s'][1] - r['s'][0] + 1)
                             for r in accepted_ranges)
    return total_combinations

print(f"Part 2 - Total Combinations: {process_ranges(workflows)}")