from dataclasses import dataclass
from decimal import Decimal
from typing import Callable, Iterable, Literal, TypedDict

from ..constants import ROUNDING_LIM
from .range import Range
from functools import partial
from ..helpers.directions import Direction
from ..helpers.utils import keys_from_value, tuple_to_decimal

AxisNames = Literal["x", "y", "x", "y"]


@dataclass
class Coordinate:
    x: Decimal
    y: Decimal

    @classmethod
    def create_coordinate(cls, x: float, y: float):
        return cls(*tuple_to_decimal(x, y))


@dataclass(frozen=True)
class Domain:
    x: Range
    y: Range
    name: str = ""

    def __repr__(self) -> str:
        return f"Domain({self.name}, x={self.x}, y={self.y})"

    def __getitem__(self, i):
        return getattr(self, i)

    @property
    def area(self):
        return self.x.size * self.y.size

    def compare_domains(self, other, consider_overlap=False):
        x_res = self.x.compare_ranges(other.x, consider_overlap)
        y_res = self.y.compare_ranges(other.y, consider_overlap)
        xd = partial(get_domain_from_range, "x", self, other)
        yd = partial(get_domain_from_range, "y", self, other)

        return ComparedDomain(
            NORTH=yd(y_res.Greater),
            SOUTH=yd(y_res.Lesser),
            EAST=xd(x_res.Greater),
            WEST=xd(x_res.Lesser),
        )

    def get_other_axis(self, axis):
        axes = {i for i in self.__annotations__.keys() if i != "name"}
        [other_axis] = axes.difference({axis})
        return other_axis

    def modify(self, fx: Callable[[Decimal], Decimal], axis: str | None = None):
        if axis == "x":
            return self.__class__(self.x.modify(fx), self.y, self.name)
        elif axis == "y":
            return self.__class__(self.x, self.y.modify(fx), self.name)
        else:
            return self.__class__(self.x.modify(fx), self.y.modify(fx), self.name)

    def get_values(self):
        return (self.x.min, self.x.max, self.y.min, self.y.max)

    def update_one_side(self, ax, side, val):
        assert ax == "x" or ax == "y"
        if ax == "x":
            return self.__class__(self.x.update_side(side, val), self.y, self.name)
        else:
            return self.__class__(self.x, self.y.update_side(side, val), self.name)

    def to_json(self):
        d = {}
        d["x"] = (str(self.x.min), str(self.x.max))
        d["y"] = (str(self.y.min), str(self.y.max))
        d["name"] = self.name
        return d

    @classmethod
    def create_domain(cls, arr: Iterable, name=""):
        assert len(list(arr)) == 4
        x_min, x_max, y_min, y_max = arr
        return cls(
            Range.create_range(x_min, x_max), Range.create_range(y_min, y_max), name
        )

    @classmethod
    def create_domain_from_coordinate(
        cls, coord: Coordinate, x_len: Decimal, y_len: Decimal, name=""
    ):
        return cls(
            Range(coord.x, coord.x + x_len), Range(coord.y, coord.y + y_len), name
        )


@dataclass(frozen=True)
class ComparedDomain:
    NORTH: Domain | None
    SOUTH: Domain | None
    EAST: Domain | None
    WEST: Domain | None

    def __getitem__(self, i):
        return getattr(self, i)

    def __iter__(self):
        for name in list(self.__annotations__.keys()):
            yield (name, self[name])

    def __repr__(self) -> str:
        N = self.NORTH.name if self.NORTH else None
        S = self.SOUTH.name if self.SOUTH else None
        E = self.EAST.name if self.EAST else None
        W = self.WEST.name if self.WEST else None
        return f"N={N} \n S={S} \n E={E} \n W={W}"

    def get_domain_directions(self, domain: Domain):
        return [Direction[i] for i in keys_from_value(self.__dict__, domain)]

    def is_empty(self):
        if not self.NORTH and not self.SOUTH and not self.EAST and not self.WEST:
            return True

    def get_axis(self):
        if self.NORTH and self.EAST:
            return ["x", "y"]
        elif self.NORTH:
            return ["y"]
        elif self.EAST:
            return ["x"]
        else:
            return []


def get_domain_from_range(
    axis: str, domain_a: Domain, domain_b: Domain, range: Range | None
):
    if range is None:
        return None
    if domain_a == domain_b:
        raise Exception("equivalent domains not handled")
    if range == domain_a[axis]:
        return domain_a
    if range == domain_b[axis]:
        return domain_b
    else:
        raise Exception("invalid range")


class DomainJson(TypedDict):
    x: tuple[str, str]
    y: tuple[str, str]
    name: str


def create_json_doman_dict(domains: dict[str, Domain]):
    return [i.to_json() for i in domains.values()]


def recreate_domain_dict_from_json(res: list[DomainJson]):
    def recreate_domain(res: DomainJson):
        return Domain(
            x=Range.recreate_range(*res["x"]),
            y=Range.recreate_range(*res["y"]),
            name=res["name"],
        )

    return {i["name"]: recreate_domain(i) for i in res}


def get_domains_extents(domains: list[Domain]):
    def get_values(ax, side):
        return [i[ax][side] for i in domains]

    x_min = min(get_values("x", "min"))
    x_max = max(get_values("x", "max"))
    y_min = min(get_values("y", "min"))
    y_max = max(get_values("y", "min"))

    return Domain.create_domain([x_min, x_max, y_min, y_max])
