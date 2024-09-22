from dataclasses import dataclass
from decimal import Decimal
from operator import add, sub
from actions.details import Details
from new_corners.range import Range
from svg_helpers.directions import Direction, get_axis
from new_corners.domain import Domain
from actions.interfaces import (
    ActionProtocol,
    ActionType,
    CurrentDomains,
    OperationLog,
    get_action_protocol,
    get_fx_and_side,
)
from itertools import product


def create_node_operations(current_domains: CurrentDomains):
    details = Details(current_domains)
    details.run()
    trials = product(details.result, [i for i in ActionType])
    f = lambda x, y: CreateModifiedDomain(current_domains.node, x, y)
    operations: list[OperationLog] = [
        OperationLog(current_domains.node, t[1], f(*t).create_domain()) for t in trials
    ]
    return operations


class CreateModifiedDomain:
    def __init__(
        self, node: Domain, details: tuple[Decimal, Direction], action: ActionType
    ) -> None:
        self.node = node
        self.size = details[0]
        self.direction = details[1]
        self.action = get_action_protocol(action)

    def create_domain(self):
        axis = get_axis(self.direction)
        other_axis = self.node.get_other_axis(axis)

        temp_domain = {}
        temp_domain["name"] = self.node.name
        temp_domain[axis] = self.modify_range(self.node[axis])
        temp_domain[other_axis] = self.node[other_axis]

        return Domain(**temp_domain)

    def modify_range(self, range: Range):
        fx, side = get_fx_and_side(self.direction, self.action.is_attractive)

        if self.action.is_deformed:
            temp_range = {}
            other_side = range.get_other_side(side)
            temp_range[side] = fx(range[side], self.size)
            temp_range[other_side] = range[other_side]
            return Range(**temp_range)
        else:
            return Range(fx(range.min, self.size), fx(range.max, self.size))
