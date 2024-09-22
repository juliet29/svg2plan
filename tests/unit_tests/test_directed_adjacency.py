from pprint import pprint
import numpy as np
from graphtype import Graph, GraphData, NodeData, EdgeData, validate
from svg_helpers.directions import Direction, NeighborDirections, get_opposite_direction

from new_corners.domain import Domain
import networkx as nx
from itertools import combinations

import pytest

x = [0, 1.5, 3, 4.5, 6]
y = list(np.linspace(0, 12, 4))


south = Domain.create_domain(x[1], x[3], y[0], y[1], "south")
north = Domain.create_domain(x[1], x[3], y[2], y[3], "north")

west = Domain.create_domain(x[0], x[2], y[1], y[2], "west")
east = Domain.create_domain(x[2], x[4], y[1], y[2], "east")
domains = [south, north, east, west]


nodes = ["west", "east", "south", "north"]
s_nodes = [n for n in nodes if n  != "south"]
n_nodes = [n for n in nodes if n  != "north"]
e_nodes = ["east"]
w_nodes = ["west"]



@validate
def test_directed_adjacency(G: Graph[NodeData["nb_dirs"::NeighborDirections]]):  # type: ignore
    
    assert G.nodes["south"]["nb_dirs"].NORTH == n_nodes
    assert G.nodes["north"]["nb_dirs"].SOUTH == s_nodes

    assert G.nodes["east"]["nb_dirs"].WEST == w_nodes
    assert G.nodes["west"]["nb_dirs"].EAST == e_nodes


    assert G.nodes["north"]["nb_dirs"].WEST == None
    assert G.nodes["south"]["nb_dirs"].EAST == None

# def create_dr_nbs(G: nx.Graph, domain_a: Domain, domain_b: Domain):
#     cmp = domain_a.compare_domains(domain_b)
#     print(cmp)
#     drns = [Direction.NORTH, Direction.EAST]
#     for d in drns:
#         G = do_assignment(d, domain_a, domain_b, cmp, G)

#     return G

def show_G(G):
    for name, val in G.nodes(data=True):
        print(name, val)


def do_assignment(G: nx.Graph, domain_a: Domain, domain_b: Domain):
    cmp = domain_a.compare_domains(domain_b)
    for drn in [Direction.NORTH, Direction.EAST]:
        opp_drn = get_opposite_direction(drn)
        if cmp[drn.name]:
            d1, d2 = (domain_a, domain_b) if cmp[drn.name] == domain_a else (domain_b, domain_a)
            G.nodes[d1.name]["nb_dirs"][opp_drn.name].append(d2.name)
            G.nodes[d2.name]["nb_dirs"][drn.name].append(d1.name)
    return G



def init_graph():
    
    G = nx.Graph()

    nodes = "south, north, east, west".split(", ")
    node_data = [(n, {"nb_dirs": NeighborDirections()}) for n in nodes]
    G.add_nodes_from(node_data)
    show_G(G)

    return G


def create_dir_graph(G):
    combos = combinations(domains, 2)
    for i,j in combos:
        print(i.name, j.name)
        G = do_assignment(G, i, j)

    show_G(G)
    return G


        
# combos = combinations(domains, 2)
# lcombos = list(combos)
# G = nx.Graph()

# nodes = "south, north, east, west".split(", ")
# node_data = [(n, {"nb_dirs": NeighborDirections()}) for n in nodes]
# G.add_nodes_from(node_data)

# for i,j in combos:
#     G = create_dr_nbs(G, i, j)
     




