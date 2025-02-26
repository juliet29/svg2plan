from decimal import Decimal
import networkx as nx
from actions.interfaces import HOLE_ACTIONS, OVERLAP_ACTIONS, ActionDetails
from domains.domain import Domain
from identify.interfaces import Problem, ProblemType
from helpers.layout import DiGraphs, Layout
from helpers.directions import Direction
from helpers.utils import filter_none
from typing import NamedTuple


class DirectedDomain(NamedTuple):
    drn: Direction
    domain: Domain


class UniqueProblem(NamedTuple):
    size: Decimal
    nbs: tuple[DirectedDomain, DirectedDomain]
    ptype: ProblemType


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


def is_a_problem(edge, domains: dict[str, Domain], ax):
    u, v = sorted([domains[i] for i in edge], key=lambda i: i[ax].min)
    hole_dif = v[ax].min - u[ax].max
    overlap_dif = u[ax].max - v[ax].min
    if hole_dif > 0:
        sz, ptype = hole_dif, ProblemType.HOLE
    elif overlap_dif > 0:
        sz, ptype = overlap_dif, ProblemType.OVERLAP
    else:
        return None
    return UniqueProblem(sz, assign_directions(ax, u, v), ptype)


def find_problems(graphs: DiGraphs, domains):
    Gx, Gy = graphs
    x_problems = filter_none([is_a_problem(e, domains, "x") for e in Gx.edges])
    y_problems = filter_none([is_a_problem(e, domains, "y") for e in Gy.edges])
    return x_problems + y_problems


def actions_for_problems(problem: UniqueProblem):
    actions = HOLE_ACTIONS if problem.ptype == ProblemType.HOLE else OVERLAP_ACTIONS
    return [
        ActionDetails(nb.domain, nb.drn, problem.size, actions) for nb in problem.nbs
    ]


def nbs_for_problem(problem: UniqueProblem):
    return [nb.domain.name for nb in problem.nbs]


def report_problems(layout: Layout):
    holes = find_problems(layout.graphs, layout.domains)

    def prepare_problem_for_reporting(ix: int, problem: UniqueProblem):
        return Problem(
            ix,
            problem_type=problem.ptype,
            nbs=nbs_for_problem(problem),
            action_details=actions_for_problems(problem),
        )

    return [prepare_problem_for_reporting(ix, hole) for ix, hole in enumerate(holes)]
