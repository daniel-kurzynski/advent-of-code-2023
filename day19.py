from aocd import get_data, submit
from collections import deque

import re

# data = 'px{a<2006:qkq,m>2090:A,rfg}\npv{a>1716:R,A}\nlnx{m>1548:A,A}\nrfg{s<537:gd,x>2440:R,A}\nqs{s>3448:A,lnx}\nqkq{x<1416:A,crn}\ncrn{x>2662:A,R}\nin{s<1351:px,qqz}\nqqz{s>2770:qs,m<1801:hdj,R}\ngd{a>3333:R,R}\nhdj{m>838:A,pv}\n\n{x=787,m=2655,a=1222,s=2876}\n{x=1679,m=44,a=2067,s=496}\n{x=2036,m=264,a=79,s=2244}\n{x=2461,m=1339,a=466,s=291}\n{x=2127,m=1623,a=2188,s=1013}'
data = get_data(day=19, year=2023)

def parse_data(data):
    workflows_section, parts_section = data.split("\n\n")
    parts = [{k: int(v) for k, v in re.findall(r'(\w+)=(\d+)', line)} for line in parts_section.split('\n')]

    workflows = {}
    for line in workflows_section.split('\n'):
        name, rules_string = line[:-1].split('{')
        rules = [(re.match(r'(\w+)([<>]=?)(\d+):(\w+|R|A)', r).groups()) if ':' in r else (None, None, None, r) for r in rules_string.split(',')]
        workflows[name] = rules

    return workflows, parts

def process_part(part, rules):
    next_wf = "in"
    while next_wf not in ['A', 'R']:
        for attribute, operator, value, outcome in rules[next_wf]:
            if operator and eval(f"part['{attribute}']{operator}{int(value)}"):
                next_wf = outcome
                break
        else:
            next_wf = outcome
    return next_wf

workflows, parts = parse_data(data)
sum_ratings = sum(sum(part.values()) for part in parts if process_part(part, workflows) == 'A')
print(f"Part 1 - Sum of Ratings for Accepted Parts: {sum_ratings}")

def process_ranges(workflows):
    queue, accepted = deque([({'x': (1, 4000), 'm': (1, 4000), 'a': (1, 4000), 's': (1, 4000)}, 'in')]), []

    while queue:
        part_range, wf = queue.popleft()

        if wf == 'A': accepted.append(part_range)
        if wf == 'R' or wf == 'A': continue

        for attribute, operator, value, outcome in workflows[wf]:
            if operator:
                start, end, value = part_range[attribute][0], part_range[attribute][1], int(value)
                if operator == '<' and end >= value or operator == '>' and start <= value:
                    queue.append(({**part_range, attribute: (start, value - 1) if operator == '<' else (value + 1, end)}, outcome))
                    part_range = {**part_range, attribute: (value, end) if operator == '<' else (start, value)}
            else:
                queue.append((part_range, outcome))
    return sum((r['x'][1] - r['x'][0] + 1) * (r['m'][1] - r['m'][0] + 1) * (r['a'][1] - r['a'][0] + 1) * (r['s'][1] - r['s'][0] + 1) for r in accepted)

print(f"Part 2 - Total Combinations: {process_ranges(workflows)}")