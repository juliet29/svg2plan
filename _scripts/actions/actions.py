from actions.details import Details
from new_corners.range import Range
from svg_helpers.directions import get_opposite_direction
from new_corners.domain import Domain
from actions.interfaces import (
    Action,
    CurrentDomains,
    get_action_protocol,
    get_components_of_action,
)


class ExecuteAction:
    def __init__(self, current_domains: CurrentDomains, action_type: Action) -> None:
        self.current_domains = current_domains
        self.node = current_domains.node
        self.action = get_action_protocol(action_type)
        self.modified_domain: Domain
        self.run()

    def run(self):
        self.get_details()
        self.modify_domain()

    def get_details(self):
        self.details = Details(self.current_domains)
        self.direction = (
            get_opposite_direction(self.details.relative_direction)
            if self.action.is_attractive
            else self.details.relative_direction
        )

    def modify_domain(self):
        axis, self.fx, self.side = get_components_of_action(self.direction)
        opp_axis = self.node.get_other_axis(axis)

        temp_domain = {}
        temp_domain["name"] = "new_domain"
        temp_domain[axis] = self.modify_range(self.node[axis])
        temp_domain[opp_axis] = self.node[opp_axis]

        self.modified_domain = Domain(**temp_domain)

    def modify_range(self, range):
        value = self.details.problem_size
        if self.action.is_deformed:
            temp_range = {}
            temp_range[self.side] = self.fx(range[self.side], value)
            other_side = range.get_other_side(self.side)
            temp_range[other_side] = range[other_side]
            return Range(**temp_range)
        else:
            return Range(self.fx(range.min, value), self.fx(range.max, value))
