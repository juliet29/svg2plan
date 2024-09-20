from dataclasses import dataclass
from enum import Enum 
from typing import Protocol
from decimal import Decimal

from python_utils import raise_exception

from svg_helpers.directions import Direction, get_axis
from new_corners.domain import Domain


class Magnetism(Enum):
    ATTRACT  = 0
    REPEL = 1


class Operation(Protocol):
    distance: Decimal
    direction_relative_to_problem: Direction
    action_direction:  Direction

    def create_action(self):
        ...


class SingleSidedOperation(Protocol):
    distance: Decimal
    direction_relative_to_problem: Direction
    action_direction:  Direction
    action_side: Direction

    def create_action(self):
        ...




class Stretch:
    ...

class Shrink:
    ...

class Push:
    ...


class Pull:
    problem_size: Decimal
    direction_relative_to_problem: Direction
    action_direction:  Direction
    problem_domain: Domain
    node_domain: Domain

    def prepare_for_action(self):
        pass

    def execute_action(self):
        new_domain = Domain("", 0, 0)
        return new_domain


class Details:
    def __init__(self, problem_domain: Domain, node_domain: Domain) -> None:
        self.problem_domain = problem_domain
        self.node_domain = node_domain

        self.problem_size: Decimal
        self.direction_relative_to_problem: Direction
        self.action_direction:  Direction

    def get_direction_relative_to_problem(self):
        self.cmp = self.problem_domain.compare_domains(self.node_domain)
        direction = self.cmp.get_key_from_domain(self.node_domain)
        self.direction_relative_to_problem = Direction[direction]

    
    def get_problem_size(self):
        axis = get_axis(self.direction_relative_to_problem)
        match axis:
            case "y":
                self.problem_size = self.problem_domain.y.size
            case "x":
                self.problem_size = self.problem_domain.x.size
            case _:
                raise Exception("Invalid axis")



    


