from itertools import chain, groupby, pairwise
from typing import Dict, Iterable, List
from actions.interfaces import ActionType, get_action_protocol
from domains.domain import Domain
from domains.range import Range
from fixes.id_helpers import chain_flatten, get_domain_directions, get_problem_size
from fixes.interfaces import ActionDetails, Problem, ProblemType
from helpers.helpers import pairwise
from helpers.directions import (
    Direction,
    get_axis,
    get_opposite_axis,
)
import networkx as nx
from helpers.layout import Layout

SIDEHOLE_ACTIONS = [a for a in ActionType if get_action_protocol(a).is_attractive]

def split(name: str, drns: list[str]):
    return ((name, drn) for drn in drns)

def group_nodes_on_edge(G: nx.Graph):
    res = (
        (name, data["data"].get_empty_directions()) for name, data in G.nodes(data=True)
    )
    filtered_res = (r for r in res if r[1] != [])
    split_res = chain.from_iterable(split(*i) for i in filtered_res)
    sorted_res = sorted(split_res, key=lambda x: x[1])

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


def check_for_side_holes(layout: Layout) -> List[tuple[Domain, Domain, str]]:
    drns_and_grouped_nodes = group_nodes_on_edge(layout.graph)
    sorted_domains_and_axes = [
        sort_domains(layout.domains, *i) for i in drns_and_grouped_nodes
    ]
    return chain_flatten([check_adjacencies(*i) for i in sorted_domains_and_axes])


def create_hole_geom(domain_a: Domain, domain_b: Domain, axis):
    a, b = sorted([domain_a, domain_b], key=lambda d: d[axis].min)
    if axis == "x":
       return Domain(Range(a.x.max, b.x.min), Range(a.y.min, b.y.max), "problem")
    else:
        return Domain(Range(a.x.min, b.x.max), Range(a.y.max, b.y.min), "problem")


def create_action_for_problem(pair_and_axis: tuple[Domain, Domain, str], geom: Domain):
    a,b, axis = pair_and_axis
    cmp = get_domain_directions(a, b)
    def create_action_details(domain: Domain):
        drns = cmp.get_domain_directions(domain)
        try:
            [drn] = [d for d in drns if get_axis(d) == axis]
        except:
            raise Exception("There should be obly one true dir!")

        return ActionDetails(domain, drn, get_problem_size(geom, drn), SIDEHOLE_ACTIONS)
    
    return [create_action_details(i) for i in [a,b]]


def create_side_hole_problems(layout: Layout):
    pairs_and_axes = check_for_side_holes(layout)
    geoms = [create_hole_geom(*p) for p in pairs_and_axes]
    probs: list[Problem] = []
    for ix, (pair_and_axis, geom) in enumerate(zip(pairs_and_axes, geoms)):
        a, b, _ = pair_and_axis
        prob = Problem(
            ix,
            ProblemType.SIDE_HOLE,
            nbs=[a.name, b.name],
            geometry=geom,
            action_details=create_action_for_problem(pair_and_axis, geom)
        )
        probs.append(prob)

    return probs