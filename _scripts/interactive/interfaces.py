from fractions import Fraction
from dataclasses import dataclass
from typing import Literal, NamedTuple, TypedDict
from pint import UnitRegistry
from decimal import Decimal
from helpers.shapely import ROUNDING_LIM
from enum import Enum



def rounded_decimal_from_fraction(frac: Fraction):
    return round(frac.numerator / Decimal(frac.denominator), ROUNDING_LIM)


class FootInchesDimension(NamedTuple):
    feet: Fraction
    inches: tuple[Fraction, Fraction]

    def __repr__(self) -> str:
        return f"{self.feet}ft, {format(self.inches[0])} {format(self.inches[1])}in ({self.meters}m)"

    @property
    def meters(self):
        ureg = UnitRegistry()
        total_meters = 0
        fractional_inches = sum([Fraction(i) for i in self.inches])
        inches_as_meters = (fractional_inches * ureg.inches).to(ureg.meters)
        total_meters += inches_as_meters

        feet_as_meters = (Fraction(self.feet) * ureg.feet).to(ureg.meters)
        total_meters += feet_as_meters
        return rounded_decimal_from_fraction(total_meters.magnitude)  # type: ignore


class WindowsJSON(TypedDict):
    id: int
    width: str
    height: str
    head_height: str
    opening_hieght: str 
    model: str 
    wtype: str

class DoorsJSON(TypedDict):
    id: int
    width: str
    height: str
    thickness: str
    material: str  # TODO

def to_json(obj):
    d = obj.__dict__
    for k, v in d.items():
        if hasattr(v, "feet"):
            d[k] = str(v.meters)
    return d

@dataclass
class SubsurfaceBase:
    id: int
    width: FootInchesDimension
    height: FootInchesDimension


WTypes = Literal["Casement", "Fixed", "Casement+Fixed"]

@dataclass
class WindowType(SubsurfaceBase):
    head_height: FootInchesDimension
    opening_hieght: FootInchesDimension 
    model: str 
    wtype: str

    def to_json(self) -> WindowsJSON:
        return to_json(self) # type: ignore



@dataclass
class DoorType(SubsurfaceBase):
    thickness: FootInchesDimension
    material: str  # TODO

    def to_json(self) -> DoorsJSON:
        return to_json(self) # type: ignore




@dataclass
class EdgeDetails():
    ix: int
    edge: tuple[str, str]
    axis: Literal["x", "y"]
    external: bool = False
    connectivity: bool = False
    detail: int | None = None



class SubsurfaceType(str, Enum):
    DOORS = "DOORS"
    WINDOWS = "WINDOWS"




class SubSurfacesJSON(TypedDict):
    WINDOWS: list[WindowsJSON]
    DOORS: list[DoorsJSON]