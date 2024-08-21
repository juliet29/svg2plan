from shapely import Point, Polygon
from shapely.coords import CoordinateSequence

def get_point_as_xy(point: Point):
    return tuple([i[0] for i in point.xy])

def list_coords(coords: CoordinateSequence):
    return [c for c in coords]