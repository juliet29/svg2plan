from enum import Enum
from dataclasses import dataclass
from new_corners.domain import Domain
from typing import Dict, Callable
from operator import add, sub
from svg_helpers.directions import Direction
from decimal import Decimal

ReductiveCallable = Callable[[Decimal, Decimal], Decimal]


@dataclass(frozen=True)
class CurrentDomains:
    node: Domain
    problem: Domain


class Action(Enum):
    PUSH = 1
    PULL = 2
    STRETCH = 3
    SQUEEZE = 4


@dataclass(frozen=True)
class ActionProtocol:
    is_attractive: bool
    is_deformed: bool


PROTOCOLS: Dict[Action, ActionProtocol] = {
    Action.PUSH: ActionProtocol(False, False),
    Action.PULL: ActionProtocol(True, False),
    Action.STRETCH: ActionProtocol(True, True),
    Action.SQUEEZE: ActionProtocol(False, True),
}

def get_action_protocol(action_type: Action):
    return PROTOCOLS[action_type]

def get_side_to_modify(direction: Direction):
    match direction:
        case Direction.EAST | Direction.NORTH:
            return "min"
        case Direction.WEST | Direction.SOUTH:
            return "max"
        case _:
            raise Exception("Invalid direction")




