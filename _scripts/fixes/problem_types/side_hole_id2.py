from itertools import chain, groupby, pairwise, combinations
from math import comb
from typing import Callable, Dict, Iterable

from torch import layout
from domains.domain import Domain
from helpers.helpers import pairwise
from helpers.directions import (
    Direction,
)
import networkx as nx


from helpers.layout import Layout


def axis_for_action(drn: Direction):
    match drn:
        case Direction.EAST | Direction.WEST:
            return "y"
        case Direction.NORTH | Direction.SOUTH:
            return "x"


def split(name: str, drns: list[str]):
    return ((name, drn) for drn in drns)


def group_nodes_on_edge(G: nx.Graph):
    res = (
        (name, data["data"].get_empty_directions()) for name, data in G.nodes(data=True)
    )
    filtered_res = (r for r in res if r[1] != [])
    split_res = chain.from_iterable(split(*i) for i in filtered_res)
    sorted_res = sorted(split_res, key=lambda x: x[1])

    nodes_along_drn: Iterable[Iterable[str]] = []
    drns: list[Direction] = []
    for k, g in groupby(sorted_res, key=lambda x: x[1]):
        nodes_along_drn.append(list((i[0] for i in g)))
        drns.append(Direction[k])

    return (drns, nodes_along_drn)


def sort_domains(
    domains: Dict[str, Domain], drn: Direction, nodes_along_drn: Iterable[str]
):
    axis = axis_for_action(drn)
    node_domains = [domains[node] for node in nodes_along_drn]
    return sorted(node_domains, key=lambda d: d[axis].min), axis


def check_adjacencies(sorted_domains: list[Domain], axis: str):
    return [(a, b) for a, b in pairwise(sorted_domains) if a[axis].max != b[axis].min]


def check_for_side_holes(layout: Layout):
    drns, grouped_nodes = group_nodes_on_edge(layout.graph)
    pairs = chain.from_iterable(
        [
            check_adjacencies(*(sort_domains(layout.domains, Direction(drn), nodes)))
            for drn, nodes in zip(drns, grouped_nodes)
        ]
    )

    return pairs


## test 4 by 4 grid, with one missing..


