from dataclasses import dataclass
from typing import Dict
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


@dataclass
class Domain:
    polygon: Polygon
    corners: Corners


DomainDict =  Dict[str, Domain]



