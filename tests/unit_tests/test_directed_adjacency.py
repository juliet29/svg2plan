from pprint import pprint
import numpy as np
from svg_helpers.directions import Direction, NeighborDirections, get_opposite_direction

from adjacencies.directed_adjacency import generate_directed_adjacencies

from new_corners.domain import Domain
import networkx as nx
from itertools import combinations

import pytest

x = [0, 1.5, 3, 4.5, 6]
y = list(np.linspace(0, 12, 4))


south = Domain.create_domain([x[1], x[3], y[0], y[1]], "south")
north = Domain.create_domain([x[1], x[3], y[2], y[3]], "north")
west = Domain.create_domain([x[0], x[2], y[1], y[2]], "west")
east = Domain.create_domain([x[2], x[4], y[1], y[2]], "east")
domains = [south, north, east, west]


nodes = ["west", "east", "south", "north"]
s_nodes = [n for n in nodes if n != "north"]
n_nodes = [n for n in nodes if n != "south"]
e_nodes = ["east"]
w_nodes = ["west"]


def init_graph():
    G = nx.Graph()
    node_data = [(n, {"data": NeighborDirections()}) for n in nodes]
    G.add_nodes_from(node_data)
    return G


def create_dir_graph():
    G = init_graph()
    combos = combinations(domains, 2)
    for i, j in combos:
        print(i.name, j.name)
        G = generate_directed_adjacencies(G, i, j)
    return G


# Graph[NodeData["data":NeighborDirections]]


def test_directed_adjacency():  # type: ignore
    G = create_dir_graph()
    assert sorted(G.nodes["south"]["data"].NORTH) == sorted(n_nodes)
    assert sorted(G.nodes["north"]["data"].SOUTH) == sorted(s_nodes)

    assert sorted(G.nodes["east"]["data"].WEST) == sorted(w_nodes)
    assert sorted(G.nodes["west"]["data"].EAST) == sorted(e_nodes)

    assert G.nodes["north"]["data"].WEST == []
    assert G.nodes["south"]["data"].EAST == []
