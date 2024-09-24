from decimal import Decimal
import pytest
from domains.range import nonDecimalRange, Range
from domains.domain import Domain
from actions.actions import create_node_operations
from actions.interfaces import ActionType
from actions.details import Details
from helpers.directions import Direction
from actions.interfaces import CurrentDomains
from random import randrange, seed

seed(2)


def create_range(init_sz=2, init_start=1):
    sz = randrange(init_sz, 100)
    start = randrange(init_start, 100)
    return nonDecimalRange(start, start + sz).toRange()


def create_domain(name: str):
    return Domain(create_range(), create_range(), name)


def create_test_cases(val: Decimal, dist: Decimal):
    return [val - dist, val, val + dist]


def rval():
    return randrange(1, 100)


def create_directed_domain(drn: Direction):
    prob = create_domain("prob")
    dist = Decimal(3)
    name = "node"
    match drn:
        case Direction.NORTH:
            val = prob.y.max
            f = lambda a: Range(a, a + rval())
        case Direction.SOUTH:
            val = prob.y.min
            f = lambda a: Range(a - rval(), a)
        case Direction.EAST:
            val = prob.x.max
            f = lambda a: Range(a, a + rval())
        case Direction.WEST:
            val = prob.x.min
            f = lambda a: Range(a - rval(), a)

    vals = create_test_cases(val, dist)
    ranges = [f(i) for i in vals]
    match drn:
        case Direction.NORTH | Direction.SOUTH:
            domains = [Domain(name, x=prob.x, y=i) for i in ranges]
        case Direction.EAST | Direction.WEST:
            domains = [Domain(name, y=prob.y, x=i) for i in ranges]
    return (prob, domains)


DRNS = [i for i in Direction]


@pytest.mark.parametrize("drn", DRNS)
def test_relative_direction(drn):
    prob, nodes = create_directed_domain(drn)
    for node in nodes:
        d = Details(CurrentDomains(node, prob))
        d.run()
        [res_drn] = d.relative_directions
        assert res_drn == drn
