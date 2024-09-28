from typing import Dict
from actions.interfaces import ActionType, get_action_protocol
from domains.domain import Domain
from helpers.layout import Layout
from fixes.interfaces import ActionDetails
from shapely import Polygon, intersection
from fixes.interfaces import Problem, ProblemType
import networkx as nx
from helpers.shapely import shape_to_domain
from itertools import chain
from fixes.id_helpers import chain_flatten, get_domain_directions, get_problem_size

Overlap = tuple[tuple[str, str], Domain]

OVERLAP_ACTIONS = [a for a in ActionType if not get_action_protocol(a).is_attractive]


def find_overlaps(G: nx.Graph, shapes: Dict[str, Polygon]) -> list[Overlap]:

    def is_overlapping(edge: tuple[str, str]) -> bool:
        u, v = edge
        if shapes[u].overlaps(shapes[v]):
            return True
        return False

    def get_overlap(edge: tuple[str, str]) -> Overlap:
        u, v = edge
        geometry = intersection(shapes[u], shapes[v])
        assert isinstance(geometry, Polygon)
        return (edge, shape_to_domain(geometry, "problem"))

    return [get_overlap(edge) for edge in G.edges if is_overlapping(edge)]


def create_action_for_problem(overlap: Overlap, domains: Dict[str, Domain]):
    edge, shape = overlap
    a, b = [domains[i] for i in edge]
    cmp = get_domain_directions(a, b)

    def create_action_details(domain: Domain):
        drns = cmp.get_domain_directions(domain)
        return [
            ActionDetails(domain, drn, get_problem_size(shape, drn), OVERLAP_ACTIONS)
            for drn in drns
        ]

    return chain_flatten([create_action_details(i) for i in [a, b]])


def create_overlap_problems(layout: Layout):
    problems: list[Problem] = []
    overlaps = find_overlaps(layout.graph, layout.shapes)
    for ix, overlap in enumerate(overlaps):
        edge, shape = overlap
        p = Problem(ix, ProblemType.OVERLAP, list(edge), shape)
        p.action_details.extend(create_action_for_problem(overlap, layout.domains))
        problems.append(p)
    return problems
