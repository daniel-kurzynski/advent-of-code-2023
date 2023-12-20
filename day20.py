from aocd import get_data, submit
import re
from collections import deque

data = get_data(day=20, year=2023)
# data = 'broadcaster -> a, b, c\n%a -> b\n%b -> c\n%c -> inv\n&inv -> a'
# data = 'broadcaster -> a\n%a -> inv, con\n&inv -> b\n%b -> con\n&con -> output'


class Module:
    def __init__(self, name):
        self.name = name
        self.destinations = []  # Stores names of destination modules

    def receive_pulse(self, pulse, source):
        return []

    def add_destination(self, dest_name):
        self.destinations.append(dest_name)

    def register_input(self, input_name):
        pass

    def get_type(self):
        return ''

class FlipFlopModule(Module):
    def __init__(self, name):
        super().__init__(name)
        self.state = False  # False = off, True = on

    def receive_pulse(self, pulse, source):
        if pulse == 'low':
            self.state = not self.state
            next_pulse = 'high' if self.state else 'low'
            return [(self.name, dest, next_pulse) for dest in self.destinations]
        return []

class ConjunctionModule(Module):
    def __init__(self, name):
        super().__init__(name)
        self.inputs = {}  # Maps input module names to their last pulse type

    def receive_pulse(self, pulse, source):
        self.inputs[source] = pulse
        if all(p == 'high' for p in self.inputs.values()):
            next_pulse = 'low'
        else:
            next_pulse = 'high'
        return [(self.name, dest, next_pulse) for dest in self.destinations]

    def register_input(self, input_name):
        self.inputs[input_name] = 'low'

class BroadcasterModule(Module):
    def __init__(self, name):
        super().__init__(name)

    def receive_pulse(self, pulse, source):
        return [(self.name, dest, pulse) for dest in self.destinations]

def parse_data(data):
    modules = {}

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

def simulate(modules):
    pulse_queue = deque([('button', 'broadcaster', 'low')])
    low_pulse_count = 0
    high_pulse_count = 0

    while pulse_queue:
        source, destination, pulse = pulse_queue.popleft()

        # print(f"{source} -{pulse}-> {destination}")

        # Count the pulses
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

    return low_pulse_count, high_pulse_count

def simulate_runs(modules, num_simulations):
    total_low_pulses, total_high_pulses = 0, 0
    cycle_detected = False
    cycle_length = 0

    for i in range(num_simulations):
        low_pulses, high_pulses = simulate(modules)
        # print(f"Simulation {i}: {low_pulses} low, {high_pulses} high")
        total_low_pulses += low_pulses
        total_high_pulses += high_pulses

        # Check if all FlipFlopModules are in their initial state
        if all(not m.state for m in modules.values() if isinstance(m, FlipFlopModule)):
            if not cycle_detected:  # Detect the cycle only once
                print(f"Cycle detected after {i} simulations")
                cycle_detected = True
                cycle_length = i + 1  # Current iteration is part of the cycle

            if cycle_detected and cycle_length != 0:
                remaining_cycles = (num_simulations - i - 1) // cycle_length
                total_low_pulses += remaining_cycles * low_pulses
                total_high_pulses += remaining_cycles * high_pulses
                break

    return total_low_pulses, total_high_pulses



# Parse the data
modules = parse_data(data)
# print(simulate(modules))
num_simulations = 1000
low_pulses, high_pulses = simulate_runs(modules, num_simulations)
print(f"Total pulses after {num_simulations} simulations: {low_pulses} low, {high_pulses} high, {low_pulses* high_pulses} total")

