from dataclasses import dataclass
from enum import Enum
from shapely import Polygon

class ProblemType(Enum):
    OVERLAP = 0
    HOLE = 1

@dataclass
class Problem:
    index: int
    problem_type: ProblemType
    nbs: list[str]
    geometry: Polygon
    resolved: bool = False
    matched: bool = False

    def __eq__(self, value) -> bool:
        if (self.problem_type == value.problem_type 
            and self.nbs == value.nbs
            and self.geometry == value.geometry
            ):
            return True
        else:
            return False
        
    def __repr__(self) -> str:
        return f"Problem(index={self.index}, problem_type={self.problem_type}, resolved={self.resolved}, nbs={self.nbs})"
