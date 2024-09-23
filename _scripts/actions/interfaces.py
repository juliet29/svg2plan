from enum import Enum
from dataclasses import dataclass
from domains.domain import Domain
from typing import Dict, Callable, Union
from operator import add, sub
from helpers.directions import Direction
from decimal import Decimal

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
    modified_domain: Domain | None
