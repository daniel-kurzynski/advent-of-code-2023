from aocd import get_data, submit
import re

# data = 'px{a<2006:qkq,m>2090:A,rfg}\npv{a>1716:R,A}\nlnx{m>1548:A,A}\nrfg{s<537:gd,x>2440:R,A}\nqs{s>3448:A,lnx}\nqkq{x<1416:A,crn}\ncrn{x>2662:A,R}\nin{s<1351:px,qqz}\nqqz{s>2770:qs,m<1801:hdj,R}\ngd{a>3333:R,R}\nhdj{m>838:A,pv}\n\n{x=787,m=2655,a=1222,s=2876}\n{x=1679,m=44,a=2067,s=496}\n{x=2036,m=264,a=79,s=2244}\n{x=2461,m=1339,a=466,s=291}\n{x=2127,m=1623,a=2188,s=1013}'
data = get_data(day=19, year=2023)

def parse_data(data):
    workflows_section, parts_section = data.split("\n\n")

    # Process workflows
    workflow_pattern = re.compile(r'(\w+)\{(.+?)\}')
    rule_pattern = re.compile(r'(\w+)([<>]=?)(\d+):(\w+|R|A)')
    workflows = {}

    for line in workflows_section.split('\n'):
        name, rules_str = workflow_pattern.match(line).groups()
        rules = rules_str.split(',')

        rule_code = ""
        for r in rules:
            if ":" in r:
                attribute, operator, value, outcome = rule_pattern.match(r).groups()
                rule_code += f"'{outcome}' if part['{attribute}'] {operator} {value} else "
            else:
                rule_code += f"'{r}'"

        workflows[name] = lambda part,rule_code=rule_code: eval(rule_code)

    part_pattern = re.compile(r'(\w+)=(\d+)')
    parts = []
    for line in parts_section.split('\n'):
        if line:
            part_dict = dict(part_pattern.findall(line.strip("{}")))
            parts.append({k: int(v) for k, v in part_dict.items()})

    return workflows, parts

workflows, parts = parse_data(data)

def process_part(part, workflows):
    next = "in"
    while next != 'A' and next != 'R':
        next = workflows[next](part)
    return next

def main(data):
    workflows, parts = parse_data(data)
    sum_ratings = 0
    for part in parts:
        if process_part(part, workflows) == 'A':  # If part is accepted
            sum_ratings += sum(part.values())  # Sum the ratings of the part
    return sum_ratings

result = main(data)
print(f"Part 1 - Sum of Ratings for Accepted Parts: {result}")
