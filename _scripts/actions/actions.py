from domains.range import InvalidRangeException, Range
from fixes.interfaces import ActionDetails
from helpers.directions import get_axis
from domains.domain import Domain
from actions.interfaces import (
    ActionType,
    OperationLog,
    get_action_protocol,
    get_fx_and_side,
)

def is_action_here(ops: list[OperationLog], action: ActionType):
    for o in ops:
        if o.action_type == action:
            return True
    return False


def create_node_operations(action_details: ActionDetails):
    operations: list[OperationLog] = []
    for action_type in action_details.action_types:
       cmd = CreateModifiedDomain(action_details, action_type)
       op = cmd.create_domain()
       if op is not None:
           operations.append(op)

    # if is_action_here(operations, ActionType.PUSH) and not is_action_here(operations, ActionType.SQUEEZE):
    #     raise Exception(f"Where is squeeze?") 
        
    return operations
           

class CreateModifiedDomain:
    def __init__(
        self, action_details: ActionDetails, action_type: ActionType
    ) -> None:
        self.node = action_details.node
        self.size = action_details.distance
        self.direction = action_details.direction
        self.action_type = action_type
        self.action = get_action_protocol(action_type)

    def create_domain(self):
        axis = get_axis(self.direction)
        other_axis = self.node.get_other_axis(axis)

        temp_domain = {}
        temp_domain["name"] = self.node.name
        try:
            temp_domain[axis] = self.modify_range(self.node[axis])
        except InvalidRangeException:
            print(f"Could not make domain!! for {self.node.name} of size {self.node[axis].size} doing action {self.action_type} in {axis} direction for {self.size} units")
            return None
        temp_domain[other_axis] = self.node[other_axis]
        return OperationLog(self.node, self.action_type, axis, Domain(**temp_domain))
       

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
