from shapely import Point

def get_point_as_xy(point: Point):
    return tuple([i[0] for i in point.xy])