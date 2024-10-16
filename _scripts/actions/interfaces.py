from collections import Counter
from enum import Enum
from dataclasses import dataclass
from domains.domain import Domain
from typing import Dict, Callable, Union
from operator import add, sub
from fixes.interfaces import Problem
from helpers.directions import Direction
from decimal import Decimal

from helpers.helpers import chain_flatten
from helpers.layout import Layout

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


N_PROBS_WEIGHT = Decimal(0.5)
SIZE_PROBS_WEIGHT = Decimal(0.5)


@dataclass
class ResultsLog:
    operation: OperationLog
    summary: Counter[str]  # Reporter.txt
    problems: list[Problem]
    new_problems: list[Problem]
    layout: Layout
    problem_being_addressed: Problem
    # domains: Dict[str, Domain]

    @property
    def num_unresolved_problems(self):
        return len([i for i in self.problems if not i.resolved])

    @property
    def problem_size(self):
        # some double counting, but will be larger for more complex problems..
        res = chain_flatten([i.action_details for i in self.problems])
        return sum([i.distance for i in res])

    @property
    def score(self):
        return (
            N_PROBS_WEIGHT * self.num_unresolved_problems
            + SIZE_PROBS_WEIGHT * self.problem_size
        )

    def __repr__(self) -> str:
        return f"node: {self.operation.node.name}, action: {self.operation.action_type.name}, summary: {self.summary}, # unres probs: {self.num_unresolved_problems}"

    def short_message(self):
        return f"{self.operation.node.name}-{self.operation.action_type.name}-for-{self.problem_being_addressed.problem_type.name} near {self.problem_being_addressed.nbs[:2]}{self.num_unresolved_problems}-PS:{self.problem_size:.2f}-S:{self.score:.2f}"
