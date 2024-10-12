from copy import deepcopy
from decimal import Decimal
from functools import reduce
from itertools import pairwise, product
from operator import add
from typing import NamedTuple, Optional
from numpy import isin
from helpers.helpers import sort_and_group_objects
from helpers.layout import DiGraphs, DomainsDict
import networkx as nx

from placement2.neighbors import create_ranges_for_all_nodes

class DistanceToMove(NamedTuple):
    root: str
    node: str
    val: Decimal

def create_graph(domains: DomainsDict, ax):
    ranges = create_ranges_for_all_nodes(domains, ax)
    G = nx.DiGraph()
    for k, v in ranges.items():
        n1 = k
        for k1, v1 in v.items():
            n2 = k1
            G.add_edge(n1, n2, size=v1.size)

    nx.is_directed_acyclic_graph(G)
    return G


def get_distances(G: nx.DiGraph, op_fx=min):
    def segment_roots():
        roots = [n[0] for n in G.in_degree if n[1] == 0]
        non_roots = [n[0] for n in G.in_degree if n[1] != 0]
        return list(product(roots, non_roots))

    def get_paths(root, node):
        return [i for i in nx.all_simple_paths(G, root, node)]

    def get_size_of_path(path: list[str]):
        return reduce(add, [G.edges[u, v]["size"] for u, v in pairwise(path)])

    def handle_group(group: list[DistanceToMove]):
        val = op_fx([i.val for i in group])
        root, node, _ = group[0]
        return DistanceToMove(root, node, val)

    sizes: list[DistanceToMove] = []
    for pair in segment_roots():
        paths = get_paths(*pair)
        if paths:
            sz = op_fx([get_size_of_path(p) for p in paths])
            sizes.append(DistanceToMove(*pair, sz))

    groups = sort_and_group_objects(sizes, lambda n: n.node)
    return [handle_group(i) for i in groups]


def modify_domain(domains: DomainsDict, distances: list[DistanceToMove], ax):
    new_domains = deepcopy(domains)
    for g in distances:
        _, node, val = g
        if ax == "x":
            new_domains[node] = domains[node].modify(lambda x: x - val, "x")
        elif ax == "y":
            new_domains[node] = domains[node].modify(lambda x: x - val, "y")

    return new_domains


def adjust_domains(domains: DomainsDict):
    Gx = create_graph(domains, "x")
    distances_x = get_distances(Gx)
    Gy = create_graph(domains, "y")
    distances_y = get_distances(Gy)

    x_domains = modify_domain(domains, distances_x, "x")
    xy_domains = modify_domain(x_domains, distances_y, "y")

    # Gxn = create_graph(xy_domains, "x")
    # Gyn = create_graph(xy_domains, "y")

    return xy_domains,  DiGraphs(Gx, Gy)



## drawing


def create_pos(domains: DomainsDict):

    return {k: (float(v.x.min), float(v.y.min)) for k, v in domains.items()}

NodePositions = dict[str, tuple[float, float]]

def draw_digraph(G, domains:DomainsDict):
    pos = create_pos(domains)
    nx.draw(G, pos=pos)
    nx.draw_networkx_labels(G, pos, labels={n: n for n in G}, font_size=10)
    edge_labels = nx.get_edge_attributes(G, "size")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)
