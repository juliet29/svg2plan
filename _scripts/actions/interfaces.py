from enum import Enum
from dataclasses import dataclass
from new_corners.domain import Domain
from typing import Dict, Callable
from operator import add, sub
from svg_helpers.directions import Direction
from decimal import Decimal

ReductiveCallable = Callable[[Decimal, Decimal], Decimal]


@dataclass
class CurrentDomains:
    node: Domain
    problem: Domain


@dataclass
class ActionProtocol:
    is_attractive: bool
    is_deformed: bool


class Action(Enum):
    PUSH = 1
    PULL = 2
    STRETCH = 3
    SQUEEZE = 4


PROTOCOLS: Dict[Action, ActionProtocol] = {
    Action.PUSH: ActionProtocol(False, False),
    Action.PULL: ActionProtocol(True, False),
    Action.STRETCH: ActionProtocol(True, True),
    Action.SQUEEZE: ActionProtocol(False, True),
}


DIRECTED_ACTION_COMPONENT: Dict[Direction, tuple[str, ReductiveCallable, str]] = {
    Direction.NORTH: ("y", add, "max"),
    Direction.SOUTH: ("y", sub, "min"),
    Direction.EAST: ("x", add, "max"),
    Direction.WEST: ("x", sub, "min"),
}


def get_action_protocol(action_type: Action):
    return PROTOCOLS[action_type]


def get_components_of_action(direction: Direction):
    return DIRECTED_ACTION_COMPONENT[direction]
