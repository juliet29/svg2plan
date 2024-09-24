import pytest
from decimal import Decimal
from domains.domain import Domain
from actions.actions import CreateModifiedDomain
from domains.range import Range, nonDecimalRange
from helpers.directions import Direction
from actions.interfaces import CurrentDomains, ActionType
from operator import add, sub
from itertools import product


def get_operators(drn: Direction):
    return (sub, add) if drn == Direction.WEST or drn == Direction.SOUTH else (add, sub)


def get_axis(drn: Direction):
    return "y" if drn == Direction.NORTH or drn == Direction.SOUTH else "x"


def expected_domain(
    drn: Direction, action: ActionType, node: Domain, dist: Decimal, axis: str
):
    f1, f2 = get_operators(drn)
    match action:
        case ActionType.PUSH:
            return Range(f1(node[axis].min, dist), f1(node[axis].max, dist))
        case ActionType.PULL:
            return Range(f2(node[axis].min, dist), f2(node[axis].max, dist))
        case ActionType.SQUEEZE:
            match drn:
                case Direction.NORTH | Direction.EAST:
                    return Range(f1(node[axis].min, dist), node[axis].max)
                case Direction.SOUTH | Direction.WEST:
                    return Range(node[axis].min, f1(node[axis].max, dist))
        case ActionType.STRETCH:
            match drn:
                case Direction.NORTH | Direction.EAST:
                    return Range(f2(node[axis].min, dist), node[axis].max)
                case Direction.SOUTH | Direction.WEST:
                    return Range(node[axis].min, f2(node[axis].max, dist))


def generate_fixed_problem() -> tuple[Domain, Decimal]:
    return (
        Domain(
             nonDecimalRange(2, 10).toRange(), nonDecimalRange(2, 10).toRange(), "test",
        ),
        Decimal(3),
    )


DRNS = [i for i in Direction]
ACTNS = [i for i in ActionType]


@pytest.mark.parametrize("drn, action", list(product(DRNS, ACTNS)))
def test_action(drn: Direction, action: ActionType):
    node, size = generate_fixed_problem()
    cm = CreateModifiedDomain(node, (size, drn), action)
    new_dom = cm.create_domain()
    axis = get_axis(drn)
    assert new_dom[axis] == expected_domain(drn, action, node, size, axis)
