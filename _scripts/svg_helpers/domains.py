from dataclasses import dataclass
from typing import Dict, Optional

from shapely import Polygon

from decimal import Decimal

from svg_helpers.constants import ROUNDING_LIM


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

    def to_decimal_corners(self):
        return DecimalCorners(
            *[Decimal(self[i]) for i in list(self.__dataclass_fields__.keys())]
        )


@dataclass
class DecimalCorners:
    x_left: Decimal
    x_right: Decimal
    y_bottom: Decimal
    y_top: Decimal

    def __getitem__(self, i):
        return getattr(self, i)

    def __iter__(self):
        return (self[i] for i in list(self.__dataclass_fields__.keys()))

    def get_float_values(self):
        return (
            round(float(self[i]), ROUNDING_LIM)
            for i in list(self.__dataclass_fields__.keys())
        )

    def to_corners(self):
        fv = list(self.get_float_values())
        return Corners(*fv)


empty_decimal_corner = DecimalCorners(*[Decimal(i) for i in [0] * 4])


@dataclass
class Domain:
    polygon: Polygon
    corners: DecimalCorners
    new_corners: Corners = Corners(0, 0, 0, 0)


DomainDict = Dict[str, Domain]
