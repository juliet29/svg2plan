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


@dataclass()
class Problem:
    index: int
    problem_type: ProblemType # Frozen!
    nbs: list[str] # Frozen!
    geometry: Optional[Polygon] = None # Frozen!
    direction: Optional[Direction] = None # Frozen!
    resolved: bool = False

    def __eq__(self, value) -> bool:
        if (self.problem_type == value.problem_type 
            and self.nbs == value.nbs
            and self.geometry == value.geometry
            ):
            return True
        else:
            return False
        
    def custom_rep(self):
        other_data = (self.geometry if self.geometry 
                      else self.direction if self.direction 
                      else "")
        txt = f"problem_type={self.problem_type}, nbs={self.nbs}, detail={other_data}"
        return txt
        
    def __hash__(self):
        return hash(self.custom_rep())
        
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
        
    
    
        
