from aocd import get_data, submit
import re
from collections import deque
from math import lcm

data = get_data(day=20, year=2023)
# data = 'broadcaster -> a, b, c\n%a -> b\n%b -> c\n%c -> inv\n&inv -> a'
# data = 'broadcaster -> a\n%a -> inv, con\n&inv -> b\n%b -> con\n&con -> output'

class Module:
    def __init__(self, name):
        self.name = name
        self.destinations = []
        self.inputs = []

    def receive_pulse(self, pulse, source):
        return []

    def add_destination(self, dest_name):
        self.destinations.append(dest_name)

    def register_input(self, input_name):
        self.inputs.append(input_name)

    def get_type(self):
        return ''

class FlipFlopModule(Module):
    def __init__(self, name):
        super().__init__(name)
        self.turned_on = False

    def receive_pulse(self, pulse, source):
        if pulse == 'low':
            self.turned_on = not self.turned_on
            next_pulse = 'high' if self.turned_on else 'low'
            return [(self.name, dest, next_pulse) for dest in self.destinations]
        return []

    def get_type(self):
        return 'flipflop'

class ConjunctionModule(Module):
    def __init__(self, name):
        super().__init__(name)
        self.inputs_states = {}  # Maps input module names to their last pulse type

    def receive_pulse(self, pulse, source):
        self.inputs_states[source] = pulse
        if all(p == 'high' for p in self.inputs_states.values()):
            next_pulse = 'low'
        else:
            next_pulse = 'high'
        return [(self.name, dest, next_pulse) for dest in self.destinations]

    def get_type(self):
        return 'conjunction'

    def register_input(self, input_name):
        super().register_input(input_name)
        self.inputs_states[input_name] = 'low'

class BroadcasterModule(Module):
    def __init__(self, name):
        super().__init__(name)

    def receive_pulse(self, pulse, source):
        return [(self.name, dest, pulse) for dest in self.destinations]

    def get_type(self):
        return 'broadcaster'

def parse_data(data):
    modules = {"rx": Module("rx"), "output": Module("output")}

    # First Iteration: Create modules
    for line in data.split('\n'):
        parts = line.split(' -> ')
        source_name = parts[0]
        if source_name.startswith('%'):
            source_name = source_name[1:]
            module = FlipFlopModule(source_name)
        elif source_name.startswith('&'):
            source_name = source_name[1:]
            module = ConjunctionModule(source_name)
        else:
            module = BroadcasterModule(source_name)
        modules[source_name] = module

    # Second Iteration: Add destinations and register inputs
    for line in data.split('\n'):
        parts = line.split(' -> ')
        source_name = parts[0].lstrip('%&')
        destinations = parts[1].split(', ')

        for dest_name in destinations:
            modules[source_name].add_destination(dest_name)
            if dest_name in modules:
                modules[dest_name].register_input(source_name)

    return modules

def simulate(modules, result_module=None):
    pulse_queue = deque([('button', 'broadcaster', 'low')])
    low_pulse_count = 0
    high_pulse_count = 0
    result_pulse = None

    while pulse_queue:
        source, destination, pulse = pulse_queue.popleft()

        if pulse == 'low':
            low_pulse_count += 1
        elif pulse == 'high':
            high_pulse_count += 1

        if not destination in modules:
            continue

        # Propagate the pulse
        new_pulses = modules[destination].receive_pulse(pulse, source)
        for new_source, new_dest, new_pulse in new_pulses:
            pulse_queue.append((new_source, new_dest, new_pulse))
            if new_dest == result_module:
                result_pulse = new_pulse


    return low_pulse_count, high_pulse_count, result_pulse

def reset_modules(modules):
    for module in modules.values():
        if isinstance(module, FlipFlopModule):
            module.turned_on = False
        elif isinstance(module, ConjunctionModule):
            module.inputs_states = {input: 'low' for input in module.inputs}

def find_cycle(modules, max_simulations, result_module=None, required_result_pulse=None):
    reset_modules(modules)
    total_low_pulses, total_high_pulses = 0, 0

    for i in range(max_simulations):
        low_pulses, high_pulses, result_pulse = simulate(modules, result_module)
        total_low_pulses += low_pulses
        total_high_pulses += high_pulses

        # Check if all FlipFlopModules are in their initial state and if requested result pulse has required value
        if all(not m.turned_on for m in modules.values() if isinstance(m, FlipFlopModule)) and (result_module is None or result_pulse == required_result_pulse):
            # print(f"Cycle detected after {i} simulations")
            cycle_length = i + 1
            return cycle_length, total_low_pulses, total_high_pulses

    return None, total_low_pulses, total_high_pulses



def simulate_runs(modules, num_simulations):
    cycle_length, total_low_pulses, total_high_pulses = find_cycle(modules, num_simulations)

    if cycle_length is None:
        return total_low_pulses, total_high_pulses

    cycles = num_simulations // cycle_length
    remaining_simulations = num_simulations - cycles * cycle_length

    if remaining_simulations != 0:
        low_pulses, high_pulses = simulate_runs(modules, remaining_simulations)
        return cycles * total_low_pulses + low_pulses, cycles * total_high_pulses + high_pulses
    return cycles * total_low_pulses, cycles * total_high_pulses




modules = parse_data(data)
num_simulations = 1000
low_pulses, high_pulses = simulate_runs(modules, num_simulations)
print(f"Part 1 - Total pulses after {num_simulations} simulations: {low_pulses} low, {high_pulses} high, {low_pulses* high_pulses} total")

def modules_contected_to(modules, module_name):
    connected_modules = set()
    stack = [module_name]

    while stack:
        name = stack.pop()
        connected_modules.add(name)
        for input in modules[name].inputs:
            if input not in connected_modules:
                stack.append(input)

    return {name: modules[name] for name in connected_modules}


if len(modules['rx'].inputs) != 1:
    raise Exception("rx should have exactly one input")

rx_input = modules['rx'].inputs[0]

if modules[rx_input].get_type() != 'conjunction':
    raise Exception("rx input should be a conjunction")

cycles = [find_cycle(modules_contected_to(modules, m), 10000, m, 'high')[0] for m in modules[rx_input].inputs]
print(f"Part 2 - Minimum number of simulations: {lcm(*cycles)}")