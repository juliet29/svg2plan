from itertools import chain, groupby, pairwise
from typing import Dict, Generator, Iterable, Literal, Type

from domains.range import Range
from domains.domain import Domain
from helpers.helpers import pairwise
import random
from helpers.directions import (
    Direction,
    NeighborDirections,
    get_axis,
    get_opposite_direction,
)
from graphtype import NodeData, Graph
import networkx as nx
from pipe import select, map, where, sort
from dataclasses import dataclass

from helpers.layout import Layout


# get nodes on the edges => return dict of n, e, w, s nodes..
# fx for anyone direction

# arrange the nodes on each side based on starting x (OR Y)
# check if each are contiguos
# x max of one => x min of the next
# otherwise, have found a side hole..

# now to get its geometry..
# can reconstruct it based on the difference in the domains.
# or to be more accurate can actually easily draw the test line,
# to ensure most coverage, do x.max, y.min  of one, and x.min, y.max of the other..
# and switch x,y for vertical vs horz..
# ag_node_data = Literal["data"]
# AGNodeType = Dict[ag_node_data, NeighborDirections]
# g = Type[Graph]
# NodeData[ag_node_data, NeighborDirections]
# TODO create dynamic literals.. and pass these around..
# g = nx.Graph()


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
    # sorted_res = sorted(res, key)


# Literal[*(Direction._member_names_)]


def sort_domains(
    domains: Dict[str, Domain], drn: Direction, nodes_along_drn: Iterable[str]
):
    axis = axis_for_action(drn)
    print(drn, axis)
    node_domains = [domains[node] for node in nodes_along_drn]
    return sorted(node_domains, key=lambda d: d[axis].min), axis


def check_adjacencies(sorted_domains: list[Domain], axis: str):
    return [(a, b) for a, b in pairwise(sorted_domains) if a[axis].max != b[axis].min]


def check_for_side_holes(layout: Layout):
    drns, grouped_nodes = group_nodes_on_edge(layout.graph)
    # sort_domains(layout.domains, Direction(drn), nodes)
    #         )
    pairs = chain.from_iterable([
        check_adjacencies(*(sort_domains(layout.domains, Direction(drn), nodes)))
        for drn, nodes in zip(drns, grouped_nodes)
    ])
    # print(pairs)

    return pairs

    # print(grouped_nodes)
    # return [
    #     (drn, nodes)
    #     for drn, nodes in grouped_nodes
    # ]

    # sorted_res = sorted(res)
    # print(sorted_res)
    # # return sor
    # get_drn_pairs = lambda name, data: (name, data["data"].get_empty_directions())
    # get_drn_pairs = lambda val: (val[0], data["data"].get_empty_directions())
    # init_list = [AGNodeData(name, data) for name, data in G.nodes(data=True)]
    # res = list(init_list | where(lambda x : x.data != [])| map(get_drn_pairs) )
    # print(res)
    # return res

    # f = lambda x: (x[0]+x[1], x[0]+x[1])
    # res = list( ((1,2), (1, 2))|  select(f) | sorted)
    # print(res)


# TODO - literals and clis in python

# xs = [0, 2, 4, 6, 8]
# ranges = [Range.create_range(*i) for i in pairwise(xs)]
# random.shuffle(ranges)

# f = lambda x: x.min
# res = sorted(ranges, key=f)
