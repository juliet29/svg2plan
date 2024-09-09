from dataclasses import dataclass
from typing import Dict, Optional

from shapely import Polygon

from decimal import Decimal

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
    
    def get_decimal_values(self):
        return (Decimal(self[i]) for i in list(self.__dataclass_fields__.keys()))
    


@dataclass
class Domain:
    polygon: Polygon
    corners: Corners
    new_corners: Corners = Corners(0,0,0,0)



DomainDict =  Dict[str, Domain]



