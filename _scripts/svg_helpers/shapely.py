from shapely import Point, Polygon, box
from shapely.coords import CoordinateSequence
from svg_helpers.domains import Corners, DecimalCorners
from svg_helpers.constants import ROUNDING_LIM
from decimal import Decimal


def get_point_as_xy(point: Point):
    return tuple([i[0] for i in point.xy])


def list_coords(coords: CoordinateSequence):
    return [c for c in coords]


def create_box_from_corners(corners: Corners):
    return box(corners.x_left, corners.y_bottom, corners.x_right, corners.y_top)


def bounds_to_corners(val: tuple):
    minx, miny, maxx, maxy = val
    return Corners(minx, maxx, miny, maxy)


def create_box_from_decimal_corners(corners: DecimalCorners) -> Polygon:
    x_left, x_right, y_bottom, y_top = corners.get_float_values()
    return box(x_left, y_bottom, x_right, y_top)


def bounds_to_decimal_corners(val: tuple):
    minx, miny, maxx, maxy = val
    f = lambda x: round(Decimal(x), ROUNDING_LIM)
    return DecimalCorners(*[f(i) for i in (minx, maxx, miny, maxy)])


def bounds_to_corners_round(val: tuple):
    minx, miny, maxx, maxy = val
    temp = [minx, maxx, miny, maxy]
    temp = [round(i, 3) for i in temp]
    return Corners(*temp)
