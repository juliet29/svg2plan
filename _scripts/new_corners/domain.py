from dataclasses import dataclass
from new_corners.range import Range
from functools import partial
from svg_helpers.helpers import keys_from_value
from log_setter.log_settings import logger


@dataclass(frozen=True)
class Domain:
    name: str
    x: Range
    y: Range

    def __repr__(self) -> str:
        return f"Domain({self.name}, x={self.x}, y={self.y})"

    def __getitem__(self, i):
        return getattr(self, i)

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


@dataclass(frozen=True)
class ComparedDomain:
    NORTH: Domain | None
    SOUTH: Domain | None
    EAST: Domain | None
    WEST: Domain | None

    def __repr__(self) -> str:
        N = self.NORTH.name if self.NORTH else None
        S = self.SOUTH.name if self.SOUTH else None
        E = self.EAST.name if self.EAST else None
        W = self.WEST.name if self.WEST else None
        return f"N={N} \n S={S} \n E={E} \n W={W}"

    def get_domain_directions(self, domain: Domain):
        return keys_from_value(self.__dict__, domain)

    def is_empty(self):
        if not self.NORTH and not self.SOUTH and not self.EAST and not self.WEST:
            return True


def get_domain_from_range(
    axis: str, domain_a: Domain, domain_b: Domain, range: Range | None
):
    if range == None:
        return None
    if domain_a == domain_b:
        raise Exception("equivalent domains not handled")
    if range == domain_a[axis]:
        return domain_a
    if range == domain_b[axis]:
        return domain_b
    else:
        raise Exception("invalid range")
