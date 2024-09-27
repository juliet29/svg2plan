from itertools import chain, groupby, pairwise
from typing import Dict, Iterable, List
from shapely import LineString, STRtree, union_all, Polygon
from domains.domain import Domain
from domains.range import Range
from fixes.interfaces import Problem, ProblemType
from helpers.helpers import pairwise
from helpers.directions import (
    Direction,
    get_axis,
    get_opposite_axis,
)
import networkx as nx
from helpers.layout import Layout
from helpers.shapely import domain_to_shape


def split(name: str, drns: list[str]):
    return ((name, drn) for drn in drns)


def group_nodes_on_edge(G: nx.Graph):
    res = (
        (name, data["data"].get_empty_directions()) for name, data in G.nodes(data=True)
    )
    filtered_res = (r for r in res if r[1] != [])
    split_res = chain.from_iterable(split(*i) for i in filtered_res)
    sorted_res = sorted(split_res, key=lambda x: x[1])
    # print("hi")

    keys_and_groups: List[tuple[Direction, Iterable[str]]] = []
    for k, g in groupby(sorted_res, key=lambda x: x[1]):
        key = Direction[k]
        group = list((i[0] for i in g))
        keys_and_groups.append((key, group))

    return keys_and_groups


def sort_domains(
    domains: Dict[str, Domain], drn: Direction, nodes_along_drn: Iterable[str]
):
    axis = get_opposite_axis(get_axis(drn))
    node_domains = [domains[node] for node in nodes_along_drn]
    return sorted(node_domains, key=lambda d: d[axis].min), axis


def check_adjacencies(
    sorted_domains: list[Domain], axis: str
) -> list[tuple[Domain, Domain, str]]:
    return [
        (a, b, axis) for a, b in pairwise(sorted_domains) if a[axis].max != b[axis].min
    ]


# def get_axes(drns: List[Direction]):
#     return [get_opposite_axis(get_axis(drn)) for drn in drns]


def chain_flatten(lst: List[List]):
    return list(chain.from_iterable(lst))


def check_for_side_holes(layout: Layout) -> List[tuple[Domain, Domain, str]]:
    drns_and_grouped_nodes = group_nodes_on_edge(layout.graph)
    sorted_domains_and_axes = [
        sort_domains(layout.domains, *i) for i in drns_and_grouped_nodes
    ]
    return chain_flatten([check_adjacencies(*i) for i in sorted_domains_and_axes])


## ---- shapely geom


def find_geometric_holes(shapes: list[Polygon]):
    union = union_all(shapes)
    difference = union.convex_hull.difference(union)
    if not difference:  # type: ignore
        print("Invalid geometry for difference in sidehole!")
        raise Exception("Invalid geometry for difference")
    try:
        assert difference.exterior  # type: ignore
        return Polygon(difference)
    except:
        return STRtree(difference.geoms)  # type: ignore


def create_test_line(domain_a: Domain, domain_b: Domain, axis):
    a, b = sorted([domain_a, domain_b], key=lambda d: d[axis].min)
    # f1 = lambda domain: [domain.x.max, domain.y.min]
    # f2 = lambda domain: [domain.x.min, domain.y.max]

    if axis == "x":
        pt1 = [a.x.max, a.y.min]  # f1(a)
        pt2 = [b.x.min, b.y.max]  # f2(b)
    else:
        pt1 = [a.x.min, a.y.max]  # f2(a)
        pt2 = [b.x.max, b.y.min]  # f1(b)

    return LineString([pt1, pt2])

def create_between_geom(domain_a: Domain, domain_b: Domain, axis):
    a, b = sorted([domain_a, domain_b], key=lambda d: d[axis].min)

    if axis == "x":
        d = Domain(Range(a.x.max, b.x.min), Range(a.y.min, b.y.max), "problem")
        
    else:
        d = Domain(Range(a.x.min, b.x.max), Range(a.y.max, b.y.min), "problem")

        # TODO should just return domains from problems.. bc flip it on the other side anyway (in StudyOneProbkem)
    return domain_to_shape(d)


def match_geometry(
    domain_a: Domain, domain_b: Domain, axis: str, geom: STRtree | Polygon
):
    try:
        assert not isinstance(geom, STRtree)
        assert geom.exterior
        return Polygon(geom)
    except:
        assert not isinstance(geom, Polygon)
        test_line = create_test_line(domain_a, domain_b, axis)
        ix = geom.nearest(test_line)
        return Polygon(geom.geometries.take(ix))


## integrate ---
def get_pair_names(pair: tuple[Domain, Domain]):
    a, b = pair
    return [a.name, b.name]


def get_axis_for_pair(drns, grouped_nodes, pair):
    p1, p2 = pair
    for ix, g in enumerate(grouped_nodes):
        if p1 and p2 in g:
            drn = drns[ix]
    return get_opposite_axis(get_axis(drn))


def get_side_hole_problems(layout: Layout):
    pairs_and_axes = check_for_side_holes(layout)
    geoms = [create_between_geom(*p) for p in pairs_and_axes]
    probs = []
    for ix, (pair_and_axis, geom) in enumerate(zip(pairs_and_axes, geoms)):
        u, v, _ = pair_and_axis
        prob = Problem(
            ix,
            ProblemType.SIDE_HOLE,
            nbs=get_pair_names((u, v)),
            direction=Direction.NORTH,
            geometry=geom,
        )
        probs.append(prob)

    return probs


# TODO simplify to functions.. 
class SideHoleIdentifier:
    def __init__(self, layout: Layout) -> None:
        self.layout = layout
        self.problems = []
        self.problem_type = "side_hole"

    def report_problems(self):
        try:
            self.problems = get_side_hole_problems(self.layout)
        except:
            self.problems = []
