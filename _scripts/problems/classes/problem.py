from dataclasses import dataclass
from typing import Optional
from enum import Enum
from shapely import Polygon
from classes.domains import Corners
from classes.directions import Direction
from svg_helpers.shapely import bounds_to_corners

class ProblemType(Enum):
    OVERLAP = 0
    HOLE = 1
    SIDE_HOLE = 2

@dataclass
class Problem:
    index: int
    problem_type: ProblemType
    nbs: list[str]
    geometry: Optional[Polygon] = None
    direction: Optional[Direction] = None
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
        txt =  f"Problem(index={self.index}, problem_type={self.problem_type}, resolved={self.resolved}, nbs={self.nbs}"
        if self.geometry:
            corner = bounds_to_corners(self.geometry.bounds)
            txt2  = (f", x_left={corner.x_left})")
        elif self.direction:
            txt2 = f", dir={self.direction.name})"
        else:
            txt2 = ")"
        return txt + txt2
        
        
