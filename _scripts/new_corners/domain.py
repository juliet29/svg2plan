from dataclasses import dataclass
from new_corners.range import Range
from functools import partial
from svg_helpers.helpers import key_from_value


@dataclass(frozen=True)
class Domain:
    name: str
    x: Range
    y: Range

    def __repr__(self) -> str:
        return f"Domain({self.name}, x={self.x}, y={self.y})"

    def __getitem__(self, i):
        return getattr(self, i)

    def compare_domains(self, other):
        x_res = self.x.compare_ranges(other.x)
        y_res = self.y.compare_ranges(other.y)
        xd = partial(get_domain_from_range, "x", self, other)
        yd = partial(get_domain_from_range, "y", self, other)

        return ComparedDomain(
            NORTH=yd(y_res.Greater),
            SOUTH=yd(y_res.Lesser),
            EAST=xd(x_res.Greater),
            WEST=xd(x_res.Lesser),
        )


@dataclass(frozen=True)
class ComparedDomain:
    NORTH: Domain | None
    SOUTH: Domain | None
    EAST: Domain | None
    WEST: Domain | None

    def __repr__(self) -> str:
        return f"{self.__dict__}"
    
    def get_key_from_domain(self, domain: Domain):
        return key_from_value(self.__dict__, domain)



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
