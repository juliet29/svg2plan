from collections import namedtuple
from typing import Dict

import networkx as nx

from ..domains.domain import Domain
from .directions import Direction, get_axis, get_opposite_axis
from .utils import chain_flatten, sort_and_group_objects

NodeandEmptyDrns = namedtuple("NodeEmptyDrns", ["node", "empty_drns"])
NodeEdgeDrn = namedtuple("NodeEdgeDrn", ["node", "drn"])


def isolate_node_and_drn(
    name: str, drns: list[str]
) -> list[NodeEdgeDrn]:  # TODO become aware of the type..
    return [NodeEdgeDrn(name, drn) for drn in drns]


def group_nodes_on_edge(G: nx.Graph) -> list[list[NodeEdgeDrn]]:
    res = [
        NodeandEmptyDrns(name, data["data"].get_empty_directions())
        for name, data in G.nodes(data=True)
    ]
    edge_nodes_and_drn = chain_flatten(
        isolate_node_and_drn(*i) for i in res if i.empty_drns
    )
    return sort_and_group_objects(edge_nodes_and_drn, lambda x: x.drn)
    # [(r[0].drn, r) for r in res2]


def sort_domains(lst: list[NodeEdgeDrn], domains: Dict[str, Domain]) -> list[Domain]:
    axis = get_opposite_axis(get_axis(Direction[lst[0].drn]))
    reverse = False if axis == "x" else True
    sorted_list = sorted(lst, key=lambda x: domains[x.node][axis].min, reverse=reverse)
    return [domains[i.node] for i in sorted_list]


def sort_nodes_on_egde(
    G: nx.Graph, domains: Dict[str, Domain]
) -> Dict[str, list[Domain]]:
    grouped_nodes = group_nodes_on_edge(G)
    return {g[0].drn: sort_domains(g, domains) for g in grouped_nodes}
