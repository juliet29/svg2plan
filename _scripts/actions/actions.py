from dataclasses import dataclass
from enum import Enum
from typing import Protocol
from decimal import Decimal
from actions.details import Details
from new_corners.range import Range, create_modfified_range
from svg_helpers.directions import (
    Direction,
    get_opposite_direction,
    DIRECTION_SIDE,
    get_opposite_axis,
    get_opposite_side
)
from new_corners.domain import Domain
from actions.interfaces import CurrentDomains


class Magnetism(Enum):
    ATTRACT = 0
    REPEL = 1


class Operation(Protocol):
    distance: Decimal
    direction_relative_to_problem: Direction
    action_direction: Direction

    def create_action(self): ...


class SingleSidedOperation(Protocol):
    distance: Decimal
    direction_relative_to_problem: Direction
    action_direction: Direction
    action_side: Direction

    def create_action(self): ...


class Pull: ...


class Shrink: ...


class Push: ...


def create_action_direction(direction: Direction, magnetism: Magnetism):
    if magnetism == Magnetism.ATTRACT:
        return get_opposite_direction(direction)
    elif magnetism == Magnetism.REPEL:
        return direction
    else:
        raise Exception("invalid magnetism")

class Stretch:
    def __init__(self, current_domains: CurrentDomains) -> None:
        self.current_domains = current_domains
        self.node = current_domains.node
        self.action_direction: Direction
        self.new_room_domain: Domain
        self.magnetism = Magnetism.ATTRACT

    def get_details(self):
        self.details = Details(self.current_domains)
        self.details.run()

    def get_action_direction(self):
        self.action_direction = create_action_direction(
            self.details.direction_relative_to_problem, self.magnetism
        )

    def execute_action(self):
        temp = {}
        temp["name"] = "new_domain"

        axis, side, fx = DIRECTION_SIDE[self.action_direction]
        temp[axis] = create_modfified_range(self.node[axis], self.details.problem_size, fx, side) 
        
        opp_axis = self.node.get_other_axis(axis)
        temp[opp_axis] = self.node[opp_axis]

        
        self.new_room_domain = Domain(**temp)


        # if both sides were changing.. 
            # min vs max doesnt matter.. 
            # wonder if range can return its own adjustment.. 




