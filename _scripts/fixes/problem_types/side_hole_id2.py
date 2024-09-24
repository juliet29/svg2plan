from itertools import chain, groupby, pairwise, combinations
from typing import Callable, Dict, Iterable
from numpy import diff
from shapely import LineString, STRtree, union_all, Polygon
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
    # TODO change to get opp axis
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

## ---- shapely geom 

def find_geometric_holes(shapes: list[Polygon]):
    union = union_all(shapes)
    difference = union.convex_hull.difference(union)
    if not difference: # type: ignore
        raise Exception("Invalid geometry for difference")
    if isinstance(difference, Polygon):
        return Polygon
    return STRtree(difference.geoms)

def create_test_line(domain_a: Domain, domain_b: Domain, axis):
    a, b = sorted([domain_a,domain_b], key=lambda d: d[axis].min)
    print(a.name, b.name)
    # f1 = lambda domain: [domain.x.max, domain.y.min]
    # f2 = lambda domain: [domain.x.min, domain.y.max]

    if axis == "x":
        pt1 = [a.x.max, a.y.min] # f1(a)
        pt2 = [b.x.min, b.y.max] # f2(b)
    else:
        pt1 = [a.x.min, a.y.max] # f2(a)
        pt2 = [b.x.max, b.y.min] # f1(b)

    return LineString([pt1, pt2])

def match_geomety(domain_a: Domain, domain_b: Domain, axis: str, tree: STRtree):
    test_line = create_test_line(domain_a, domain_b, axis)
    ix = tree.nearest(test_line)
    return Polygon(tree.geometries.take(ix))

    
    
