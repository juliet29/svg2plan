from copy import deepcopy
from typing import Optional
import networkx as nx
from itertools import product
from itertools import chain

from fixes.interfaces import Direction
from helpers.helpers import chain_flatten
from helpers.layout import Layout
from helpers.layout import DomainsDict
from placement.attract import draw_digraph
from domains.domain import AxisNames




def get_roots_and_leaves_for_dag(G: nx.DiGraph):
    roots = [n[0] for n in G.in_degree if n[1] == 0]
    leaves = [n[0] for n in G.out_degree if n[1] == 0]
    return (roots, leaves)


def handle_missing_nodes(G: nx.DiGraph, domains: DomainsDict, ax: AxisNames):
    diff = set(domains.keys()).difference(set(G.nodes))
    if not diff:
        return []
    
    def create_x_edges(node):
        return [(Direction.WEST.name, node),
        (node, Direction.EAST.name)]
    
    def create_y_edges(node):
        return [(Direction.SOUTH.name, node),
        (node, Direction.NORTH.name)]
    
    if ax == "x":
        return chain_flatten([create_x_edges(i) for i in diff])
    else:
        return chain_flatten([create_y_edges(i) for i in diff])

    



def create_dag_with_cardinal_directions(G: nx.DiGraph, domains: DomainsDict, ax: AxisNames):
    drn1, drn2 = (
        (Direction.WEST, Direction.EAST)
        if ax == "x"
        else (Direction.SOUTH, Direction.NORTH)
    )
    roots, leaves = get_roots_and_leaves_for_dag(G)
    edges = chain.from_iterable(
        [product([drn1.name], roots), product(leaves, [drn2.name])]
    )

    Gn = deepcopy(G)
    Gn.add_nodes_from([drn1.name, drn2.name])
    Gn.add_edges_from(edges)

    missing_edges = handle_missing_nodes(G, domains, ax)
    Gn.add_edges_from(missing_edges)

    return Gn




def create_cardinal_dags(layout: Layout):
    domains, [Gx, Gy] = layout
    Gxd = create_dag_with_cardinal_directions(Gx, domains, "x")
    Gyd = create_dag_with_cardinal_directions(Gy, domains, "y")
    return Gxd, Gyd

