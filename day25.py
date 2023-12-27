from aocd import get_data, submit
import re
import networkx as nx
import random

from itertools import chain, combinations

# data = 'jqt: rhn xhk nvd\nrsh: frs pzl lsr\nxhk: hfx\ncmg: qnr nvd lhk bvb\nrhn: xhk bvb hfx\nbvb: xhk hfx\npzl: lsr hfx nvd\nqnr: nvd\nntq: jqt hfx bvb xhk\nnvd: lhk\nlsr: lhk\nrzs: qnr cmg lsr rsh\nfrs: qnr lhk lsr'
data = get_data(day=25, year=2023)

def parse_data(data):
    nodes = set()
    graph = nx.Graph()

    for line in data.split('\n'):
        component, connected = line.split(': ')
        connected = connected.split(' ')
        nodes.add(component)
        for node in connected:
            graph.add_edge(component, node, capacity=1.)
            nodes.add(node)
    return graph, nodes


def find_disconnections(graph, nodes, n):
    nodes_list = list(nodes)
    for i, source in enumerate(nodes_list):
        for sink in nodes_list[i+1:]:
            cut_value, partition = nx.minimum_cut(graph, source, sink)
            if cut_value == n:
                return partition
    return None

graph, nodes = parse_data(data)
partition = find_disconnections(graph, nodes, 3)
print(f"Part 1 - Product of Group Sizes: {len(partition[0]) * len(partition[1])}")