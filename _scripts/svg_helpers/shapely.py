from shapely import Point, Polygon, box, from_wkt, geometry, to_wkt
from shapely.coords import CoordinateSequence
from new_corners.domain import Domain
from svg_helpers.domains import Corners, DecimalCorners
from svg_helpers.constants import ROUNDING_LIM
from decimal import Decimal


def get_point_as_xy(point: Point):
    return tuple([i[0] for i in point.xy])


def list_coords(coords: CoordinateSequence):
    return [c for c in coords]


# def create_box_from_corners(corners: Corners):
#     return box(corners.x_left, corners.y_bottom, corners.x_right, corners.y_top)


# def bounds_to_corners(val: tuple):
#     minx, miny, maxx, maxy = val
#     return Corners(minx, maxx, miny, maxy)



# def bounds_to_decimal_corners(val: tuple):
#     minx, miny, maxx, maxy = val
#     f = lambda x: round(Decimal(x), ROUNDING_LIM)
#     return DecimalCorners(*[f(i) for i in (minx, maxx, miny, maxy)])




# def create_box_from_decimal_corners(corners: DecimalCorners) -> Polygon:
#     c = corners
#     arr = [(c.x_right, c.y_bottom),
#     (c.x_right, c.y_top),
#     (c.x_left, c.y_top),
#     (c.x_left, c.y_bottom),
#     (c.x_right, c.y_bottom),
#     ]
#     sarr = [(str(i[0]), str(i[1])) for i in arr]
#     groups = [create_str_pair(i) for i in sarr]
#     sgroup = ", ".join(groups)
#     wkt = "POLYGON (({}))".format(sgroup)
#     shape = from_wkt(wkt)

#     assert isinstance(shape, geometry.base.BaseGeometry)
#     assert isinstance(shape, Polygon)

#     return shape

create_str_pair = lambda x: "{} {}".format(x[0], x[1])

def create_box_from_domain(domain: Domain) -> Polygon:
    c = domain
    arr = [(c.x.max, c.y.min),
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

def shape_to_domain(shape: Polygon):
    wkt = to_wkt(shape, rounding_precision=ROUNDING_LIM)
    nums = wkt.split("((")[1].split("))")[0].split(", ")
    xs, ys = [], []
    for num in nums:
        x, y = num.split(" ")
        xs.append(x)
        ys.append(y)

    x_left, x_right = min(xs), max(xs)
    y_bottom, y_top = min(ys), max(ys)
    return Domain.create_domain("", x_left, x_right, y_bottom, y_top)

