from dataclasses import dataclass, field
from decimal import Decimal
from typing import Optional
from enum import Enum
from shapely import Polygon
from actions.interfaces import ActionType, get_action_protocol
from helpers.directions import Direction
from helpers.layout import Layout
from domains.domain import Domain



class LayoutBase:
    def __init__(self, layout: Layout) -> None:
        self.G = layout.graph
        self.domains = layout.domains
        self.shapes = layout.shapes
        self.layout = layout


@dataclass
class ActionDetails:
    node: Domain
    direction: Direction
    distance: Decimal
    action_types: list[ActionType]

    def __repr__(self) -> str:
        return f"{self.node.name}-{self.direction.name}-{self.distance}"
       
class ProblemType(Enum):
    OVERLAP = 0
    HOLE = 1
    SIDE_HOLE = 2

@dataclass()
class Problem:
    index: int
    problem_type: ProblemType 
    nbs: list[str]  
    geometry: Domain 
    resolved: bool = False
    action_details: list[ActionDetails] = field(default_factory=list)

    def __eq__(self, value) -> bool:
        if (
            self.problem_type == value.problem_type
            and self.nbs == value.nbs
            and self.geometry == value.geometry
        ):
            return True
        else:
            return False

    def custom_rep(self):
        txt = f"problem_type={self.problem_type}, nbs={self.nbs}, detail={self.geometry}"
        return txt

    def __hash__(self):
        return hash(self.custom_rep())

    def __repr__(self) -> str:
        txt = f"Problem(ix={self.index}, {self.problem_type.name}, {self.nbs}, resolved={self.resolved},  n_actions={len(self.action_details)}"
        return txt

    def short_message(self):
        return f"{self.problem_type}-{self.nbs}"

OVERLAP_ACTIONS = [ActionType.PUSH, ActionType.SQUEEZE]
SIDEHOLE_ACTIONS = [ActionType.PULL, ActionType.STRETCH]