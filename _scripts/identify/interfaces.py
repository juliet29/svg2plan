from dataclasses import dataclass, field
from typing import Optional
from enum import Enum
from shapely import Polygon
from actions.interfaces import get_action_protocol
from actions.interfaces import ActionDetails
from helpers.layout import Layout
from domains.domain import Domain


class ProblemType(Enum):
    OVERLAP = 0
    HOLE = 1
    SIDE_HOLE = 2


@dataclass()
class Problem:
    index: int
    problem_type: ProblemType
    nbs: list[str]
    action_details: list[ActionDetails]
    geometry: Optional[Domain] = None  # TODO phase out
    resolved: bool = False

    def __eq__(self, value) -> bool:
        if (
            self.problem_type == value.problem_type
            and self.nbs == value.nbs
            and self.action_details == value.action_details
        ):
            return True
        else:
            return False

    def custom_rep(self):
        txt = f"problem_type={self.problem_type}, nbs={self.nbs}actions={self.action_details} "
        return txt

    def __hash__(self):
        return hash(self.custom_rep())

    def __repr__(self) -> str:
        txt = f"Problem(ix={self.index}, {self.problem_type.name}, {self.nbs}, resolved={self.resolved},  n_actions={len(self.action_details)}"
        return txt

    def short_message(self):
        return f"{self.problem_type}-{self.nbs}"
