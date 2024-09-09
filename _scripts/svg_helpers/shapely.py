from shapely import Point, Polygon, box
from shapely.coords import CoordinateSequence
from svg_helpers.domains import Corners


def get_point_as_xy(point: Point):
    return tuple([i[0] for i in point.xy])


def list_coords(coords: CoordinateSequence):
    return [c for c in coords]


def create_box_from_corners(corners: Corners):
    return box(corners.x_left, corners.y_bottom, corners.x_right, corners.y_top)


def bounds_to_corners(val: tuple):
    minx, miny, maxx, maxy = val
    return Corners(minx, maxx, miny, maxy)




def bounds_to_corners_round(val: tuple):
    minx, miny, maxx, maxy = val
    temp = [minx, maxx, miny, maxy]
    temp = [round(i, 3) for i in temp]
    return Corners(*temp)

