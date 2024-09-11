from dataclasses import dataclass
from problems.classes.problem import Problem
from enum import Enum
from decimal import Decimal

class ActionType(Enum):
    STRETCH = 0
    PUSH = 1

@dataclass
class Action:
    problem: Problem
    action_type: ActionType
    node: str
    distance: Decimal
    succesful: bool = False

    def __repr__(self) -> str:
        txt = f"Action(problem=({self.problem.index, self.problem.problem_type.name}), action_type={self.action_type}, node={self.node}, distance={self.distance})" 
        return txt


