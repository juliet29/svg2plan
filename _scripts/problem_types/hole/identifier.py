from dataclasses import dataclass
from svg_helpers.layout import Layout
from svg_helpers.directions import Direction
from svg_helpers.layout_base import LayoutBase
from shapely import Polygon, union_all, STRtree, LinearRing
from problems.classes.problem import Problem, ProblemType
from svg_helpers.helpers import key_from_value, compare_sequences


@dataclass
class HoleData:
    shape: Polygon
    rooms: list


class HoleIdentifier(LayoutBase):
    def __init__(self, layout: Layout) -> None:
        super().__init__(layout)
        self.problems: list[Problem] = []
        self.holes: list[HoleData] = []

    def report_problems(self):
        self.find_holes()
        for ix, data in enumerate(self.holes):
            self.problems.append(
                Problem(ix, ProblemType.HOLE, nbs=data.rooms, geometry=data.shape)
            )

    def find_holes(self):
        self.union = union_all(list(self.shapes.values()))
        assert isinstance(self.union, Polygon)
        self.tree = STRtree(list(self.shapes.values()))
        for hole in self.union.interiors:
            assert isinstance(hole, LinearRing)
            self.hole = hole
            p = HoleData(
                Polygon(self.hole),
                self.find_rooms_surrounding_hole(),
            )
            self.holes.append(p)

    def find_rooms_surrounding_hole(self):
        assert isinstance(self.union, Polygon)
        indices = self.tree.query_nearest(self.hole)
        nearest = self.tree.geometries.take(indices).tolist()
        rooms = [key_from_value(self.shapes, p) for p in nearest]
        return rooms
