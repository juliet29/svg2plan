from dataclasses import dataclass
from typing import Dict, Optional
# from collections import namedtuple

from shapely import Polygon

# Corners = namedtuple("Corners", ["x_left", "x_right", "y_bottom", "y_top"])



@dataclass
class Corners:
    x_left: float
    x_right: float
    y_bottom: float
    y_top: float

    def __getitem__(self, i):
        return getattr(self, i)

    def __iter__(self):
        return (self[i] for i in list(self.__dataclass_fields__.keys()))


@dataclass
class Domain:
    polygon: Polygon
    corners: Corners
    new_corners: Corners = Corners(0,0,0,0)



DomainDict =  Dict[str, Domain]



