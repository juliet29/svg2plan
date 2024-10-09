from decimal import Decimal
import networkx as nx
from domains.domain import Domain
from fixes.interfaces import HOLE_ACTIONS, ActionDetails, Problem, ProblemType
from helpers.layout import Layout
from helpers.directions import Direction
from helpers.helpers import filter_none
from typing import NamedTuple


class DirectedDomain(NamedTuple):
    drn: Direction
    domain: Domain


class Hole(NamedTuple):
    size: Decimal
    nbs: tuple[DirectedDomain, DirectedDomain]


def assign_directions(ax, lesser, greater):
    if ax == "x":
        return (
            DirectedDomain(Direction.WEST, lesser),
            DirectedDomain(Direction.EAST, greater),
        )
    elif ax == "y":
        return (
            DirectedDomain(Direction.SOUTH, lesser),
            DirectedDomain(Direction.NORTH, greater),
        )
    else:
        raise Exception("Invalid ax")


def is_not_touching(edge, domains: dict[str, Domain], ax):
    u, v = sorted([domains[i] for i in edge], key=lambda i: i[ax].min)
    dif = v[ax].min - u[ax].max
    if dif != 0:
        return Hole(dif, assign_directions(ax, u, v))


def find_holes(Gx: nx.DiGraph, Gy: nx.DiGraph, domains):
    x_holes = filter_none([is_not_touching(e, domains, "x") for e in Gx.edges])
    y_holes = filter_none([is_not_touching(e, domains, "y") for e in Gy.edges])
    return x_holes + y_holes


def actions_for_hole(hole: Hole):
    return [
        ActionDetails(nb.domain, nb.drn, hole.size, HOLE_ACTIONS) for nb in hole.nbs
    ]


def nbs_for_hole(hole: Hole):
    return [nb.domain.name for nb in hole.nbs]


def create_hole_problems(layout: Layout):
    # TODO update layout..
    holes = find_holes(layout.graph, layout.domains)

    def define_problem_for_hole(ix: int, hole: Hole):
        return Problem(
            ix,
            ProblemType.HOLE,
            nbs=nbs_for_hole(hole),
            action_details=actions_for_hole(hole),
        )

    return [define_problem_for_hole(ix, hole) for ix, hole in enumerate(holes)]
