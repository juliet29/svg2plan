from classes.layout import Layout
from classes.directions import Direction
from problems.classes.problems_base import ProblemsBase
from shapely import Polygon, union_all, STRtree, LinearRing
from problems.classes.problem import Problem, ProblemType
from svg_helpers.helpers import key_from_value

class HoleIdentifier(ProblemsBase):
    def __init__(self, layout:Layout) -> None:
        super().__init__(layout)
        self.problems = []

    def find_holes(self):
        self.union = union_all(list(self.shapes.values()))
        assert isinstance(self.union, Polygon)

        self.tree = STRtree(list(self.shapes.values()))

        for ix, hole in enumerate(self.union.interiors):
            assert isinstance(hole, LinearRing)
            p  = Problem(
                ix,
                ProblemType.HOLE,
                self.find_rooms_surrounding_hole(),
                Polygon(hole),
            )
            self.problems.append(p)

    def find_rooms_surrounding_hole(self):
        assert isinstance(self.union, Polygon)
        indices = self.tree.query_nearest(self.union.interiors[0])
        nearest = self.tree.geometries.take(indices).tolist()
        rooms = [key_from_value(self.shapes, p) for p in nearest]
        return rooms