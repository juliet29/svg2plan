from copy import deepcopy
from decimal import Decimal, localcontext
from statistics import mean
from domains.domain import Domain
from helpers.directions import Direction
import networkx as nx
from helpers.layout import DiGraphs
from placement2.attract import DomainsDict
from placement2.connectivity import create_cardinal_dags


def normalize_to_target(arr):
    # log scale might be better..
    with localcontext() as ctx:
        ctx.prec = 3
        r_min, r_max = min(arr), max(arr)
        t_min, t_max = Decimal("0.1"), 1
        normalize = lambda x: (x - r_min) / (r_max - r_min)
        scale = lambda x: (normalize(x) * (t_max - t_min)) + t_min
        return [scale(i) for i in arr]


def get_edge_nodes(graphs: DiGraphs, domains: DomainsDict):
    Gxc, Gyc = create_cardinal_dags(*graphs)
    nodes = {}

    nodes[Direction.WEST] = [domains[e[1]] for e in Gxc.edges if "WEST" in e]
    nodes[Direction.EAST] = [domains[e[0]] for e in Gxc.edges if "EAST" in e]

    nodes[Direction.SOUTH] = [domains[e[1]] for e in Gyc.edges if "SOUTH" in e]
    nodes[Direction.NORTH] = [domains[e[0]] for e in Gyc.edges if "NORTH" in e]

    return nodes


def smooth_edge(nodes: list[Domain], drn: Direction, domains: DomainsDict):
    weights = normalize_to_target([i.area for i in nodes])
    vals = [i.x.min for i in nodes]
    val = mean([w * x for w, x in zip(weights, vals)])

    match drn:
        case Direction.SOUTH:
            ax, side = "y", min
        case Direction.WEST:
            ax, side = "x", min
        case Direction.NORTH:
            ax, side = "y", max
        case Direction.EAST:
            ax, side = "x", min

    new_nodes = [i.update_one_side(ax, side, val) for i in nodes] 

    new_domains = deepcopy(domains)
    for node in new_nodes:
        new_domains[node.name] = node

    return new_domains


def level_sides(graphs: DiGraphs, domains: DomainsDict):
    nodes_dict = get_edge_nodes(graphs, domains)
    for drn, nodes in nodes_dict.items():
        domains = smooth_edge(nodes, drn, domains)

    return domains


