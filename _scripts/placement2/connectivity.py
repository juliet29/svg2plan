from copy import deepcopy
from decimal import Decimal
from typing import Optional
import networkx as nx
from itertools import product
from itertools import chain

from domains.domain import Domain
from fixes.interfaces import Direction
from placement2.attract import DomainsDict, create_pos, draw_digraph
# from matplotlib.pyplot import subplot


def get_roots_and_leaves_for_dag(G: nx.DiGraph):
    roots = [n[0] for n in G.in_degree if n[1] == 0]
    leaves = [n[0] for n in G.out_degree if n[1] == 0]
    return (roots, leaves)


def create_dag_with_cardinal_directions(G: nx.DiGraph, ax):
    drn1, drn2 = (
        (Direction.WEST, Direction.EAST)
        if ax == "x"
        else (Direction.SOUTH, Direction.NORTH)
    )
    roots, leaves = get_roots_and_leaves_for_dag(G)
    edges = chain.from_iterable([
        product([drn1.name], roots), 
        product(leaves, [drn2.name])
        ])

    Gn = deepcopy(G)
    Gn.add_nodes_from([drn1.name, drn2.name])
    Gn.add_edges_from(edges)
    return Gn


NodePositions = dict[str, tuple[float, float]]


def get_bounds_of_positioned_graph(pos: NodePositions):
    x_values = [coord[0] for coord in pos.values()]
    y_values = [coord[1] for coord in pos.values()]

    x_min = min(x_values)
    x_max = max(x_values)
    y_min = min(y_values)
    y_max = max(y_values)

    return Domain.create_domain([x_min, x_max, y_min, y_max])


def create_tuple_of_floats(u, v):
    return (float(u), float(v))


def create_cardinal_positions(
    pos: Optional[NodePositions] = None, domains:Optional[DomainsDict] = None, padding:float = 1.0
):
    if not pos:
        assert domains, "Must have domians if pos not passed"
        new_pos = create_pos(domains)
    else:
        new_pos = deepcopy(pos)

    c = get_bounds_of_positioned_graph(new_pos)
    mid_x = ((c.x.max - c.x.min) / 2) + c.x.min
    mid_y = ((c.y.max - c.y.min) / 2) + c.y.min

    PAD = Decimal(padding)

    values = [
        (mid_x, c.y.max + PAD),
        (mid_x, c.y.min - PAD),
        (c.x.min - PAD, mid_y),
        (c.x.max + PAD, mid_y),
    ]
    res = [create_tuple_of_floats(*i) for i in values]


    new_pos[Direction.NORTH.name] = res[0]
    new_pos[Direction.SOUTH.name] = res[1]
    new_pos[Direction.WEST.name] = res[2]
    new_pos[Direction.EAST.name] = res[3]

    return new_pos

def create_cardinal_dags(Gx: nx.DiGraph, Gy: nx.DiGraph ):
    Gxd = create_dag_with_cardinal_directions(Gx, "x")
    Gyd = create_dag_with_cardinal_directions(Gy, "y")
    return Gxd, Gyd

def draw_graph_with_node_labels(G, pos, ):
    nx.draw(G, pos=pos)
    nx.draw_networkx_labels(G, pos, labels={n: n for n in G}, font_size=10)

# def draw_cardinal_dags(Gx: nx.DiGraph, Gy: nx.DiGraph,domains: DomainsDict):
#     pos=create_cardinal_positions(domains=domains, padding=2)
#     subplot(121)
#     draw_graph_with_node_labels(Gx, pos=pos)
#     subplot(122)
#     draw_graph_with_node_labels(Gy, pos=pos)





