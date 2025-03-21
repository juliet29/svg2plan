from shapely import Point, Polygon, from_wkt, geometry, to_wkt, unary_union
from shapely.coords import CoordinateSequence

from svg2plan.domains.range import InvalidRangeException

from ..constants import ROUNDING_LIM
from ..domains.domain import Domain


def get_point_as_xy(point: Point):
    return tuple([i[0] for i in point.xy])


def list_coords(coords: CoordinateSequence):
    return [c for c in coords]


def create_str_pair(x):
    return "{} {}".format(x[0], x[1])


def domain_to_shape(domain: Domain) -> Polygon:
    c = domain
    arr = [
        (c.x.max, c.y.min),
        (c.x.max, c.y.max),
        (c.x.min, c.y.max),
        (c.x.min, c.y.min),
        (c.x.max, c.y.min),
    ]
    sarr = [(str(i[0]), str(i[1])) for i in arr]
    groups = [create_str_pair(i) for i in sarr]
    sgroup = ", ".join(groups)
    wkt = "POLYGON (({}))".format(sgroup)
    shape = from_wkt(wkt)

    assert isinstance(shape, geometry.base.BaseGeometry)
    assert isinstance(shape, Polygon)

    return shape

def domains_to_shape(domains: list[Domain]):
    return unary_union([domain_to_shape(i) for i in domains]) 


def shape_to_domain(shape: Polygon, name: str = ""):
    wkt = to_wkt(shape, rounding_precision=ROUNDING_LIM)
    nums = wkt.split("((")[1].split("))")[0].split(", ")
    xs, ys = [], []
    for num in nums:
        x, y = num.split(" ")
        xs.append(x)
        ys.append(y)

    x_left, x_right = min(xs), max(xs)
    y_bottom, y_top = min(ys), max(ys)
    try:
        return Domain.create_domain([x_left, x_right, y_bottom, y_top], name)
    except InvalidRangeException:
        return Domain.create_domain([x_left, x_right, y_top, y_bottom], name)
