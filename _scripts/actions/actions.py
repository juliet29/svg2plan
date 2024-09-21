from operator import add, sub
from actions.details import Details
from new_corners.range import Range
from svg_helpers.directions import get_axis
from new_corners.domain import Domain
from actions.interfaces import (
    ActionType,
    CurrentDomains,
    get_action_protocol,
    get_fx_and_side,
)


class ExecuteAction:
    def __init__(
        self, current_domains: CurrentDomains, action_type: ActionType
    ) -> None:
        self.current_domains = current_domains
        self.node = current_domains.node
        self.modified_domain: Domain

        self.details = Details(self.current_domains)
        self.action = get_action_protocol(action_type)
        self.modify_domain()

    def modify_domain(self):
        axis = get_axis(self.details.relative_direction)
        other_axis = self.node.get_other_axis(axis)

        temp_domain = {}
        temp_domain["name"] = "new_domain"
        temp_domain[axis] = self.modify_range(self.node[axis])
        temp_domain[other_axis] = self.node[other_axis]

        self.modified_domain = Domain(**temp_domain)

    def modify_range(self, range):
        fx, side = get_fx_and_side(
            self.details.relative_direction, self.action.is_attractive
        )
        value = self.details.problem_size

        if self.action.is_deformed:
            temp_range = {}
            other_side = range.get_other_side(side)
            temp_range[side] = fx(range[side], value)
            temp_range[other_side] = range[other_side]
            return Range(**temp_range)
        else:
            return Range(fx(range.min, value), fx(range.max, value))
