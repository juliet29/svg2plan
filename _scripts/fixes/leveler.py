from copy import deepcopy
from decimal import Decimal, localcontext
from statistics import mean
from helpers.directions import Direction
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


def get_edge_nodes(graphs: DiGraphs):
    Gxc, Gyc = create_cardinal_dags(*graphs)
    nodes = {}

    nodes[Direction.WEST] = [e[1] for e in Gxc.edges if "WEST" in e]
    nodes[Direction.EAST] = [e[0] for e in Gxc.edges if "EAST" in e]

    nodes[Direction.SOUTH] = [e[1] for e in Gyc.edges if "SOUTH" in e]
    nodes[Direction.NORTH] = [e[0] for e in Gyc.edges if "NORTH" in e]

    return nodes

def to_rounded_decimal(val:float):
    return round(Decimal(val), 2)

def smooth_edge(node_names: list[str], drn: Direction, domains: DomainsDict):
    nodes = [domains[i] for i in node_names]

    match drn:
        case Direction.SOUTH:
            ax, side = "y", "min"
        case Direction.WEST:
            ax, side = "x", "min"
        case Direction.NORTH:
            ax, side = "y", "max"
        case Direction.EAST:
            ax, side = "x", "max"

    
    # TODO - weights = normalize_to_target([i.area for i in nodes])
    vals = [i[ax][side] for i in nodes]
    weights = [1 for i in nodes]
    val = to_rounded_decimal(mean([w * x for w, x in zip(weights, vals)]))
    print(drn, val)


    new_nodes = [i.update_one_side(ax, side, val) for i in nodes] 

    for node in new_nodes:
        domains[node.name] = node

    return domains


def level_sides(graphs: DiGraphs, domains: DomainsDict):
    nodes_dict = get_edge_nodes(graphs)

    new_doms = deepcopy(domains)
    for drn, nodes in nodes_dict.items():
        new_doms = smooth_edge(nodes, drn, new_doms)

    return new_doms



