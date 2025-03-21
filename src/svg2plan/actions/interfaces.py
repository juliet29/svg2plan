from dataclasses import dataclass
from decimal import Decimal
from enum import Enum
from operator import add, sub
from typing import Callable, Dict

from ..domains.domain import Domain
from ..helpers.directions import Direction

ReductiveCallable = Callable[[Decimal, Decimal], Decimal]


@dataclass(frozen=True)
class CurrentDomains:
    node: Domain
    problem: Domain


class ActionType(Enum):
    PUSH = 1
    PULL = 2
    STRETCH = 3
    SQUEEZE = 4


@dataclass(frozen=True)
class ActionProtocol:
    is_attractive: bool
    is_deformed: bool


PROTOCOLS: Dict[ActionType, ActionProtocol] = {
    ActionType.PUSH: ActionProtocol(False, False),
    ActionType.PULL: ActionProtocol(True, False),
    ActionType.STRETCH: ActionProtocol(True, True),
    ActionType.SQUEEZE: ActionProtocol(False, True),
}


def get_action_protocol(action_type: ActionType):
    return PROTOCOLS[action_type]


def is_upper(direction: Direction):
    match direction:
        case Direction.EAST | Direction.NORTH:
            return True
        case Direction.WEST | Direction.SOUTH:
            return False
        case _:
            raise Exception("Invalid direction")


def get_fx_and_side(direction: Direction, is_attractive: bool):
    match is_upper(direction), is_attractive:
        case (True, True):
            return (sub, "min")
        case (True, False):
            return (add, "min")
        case (False, True):
            return (add, "max")
        case (False, False):
            return (sub, "max")
        case _:
            raise Exception("Invalid direction or attractiveness")


@dataclass
class OperationLog:
    node: Domain
    action_type: ActionType
    axis: str
    modified_domain: Domain


from decimal import Decimal


@dataclass
class ActionDetails:
    node: Domain
    direction: Direction
    distance: Decimal
    action_types: list[ActionType]

    def __repr__(self) -> str:
        return f"{self.node.name}-{self.direction.name}-{self.distance}"


OVERLAP_ACTIONS = [ActionType.PUSH, ActionType.SQUEEZE]
HOLE_ACTIONS = [ActionType.PULL, ActionType.STRETCH]
