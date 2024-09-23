from dataclasses import dataclass, field
from helpers.layout import Layout
from helpers.directions import Direction
from fixes.interfaces import LayoutBase
from shapely import Polygon, intersection
from fixes.interfaces import Problem, ProblemType


@dataclass
class OverlapData:
    shape: Polygon
    rooms: list


class OverlapIdentifier(LayoutBase):
    def __init__(self, layout: Layout) -> None:
        super().__init__(layout)
        self.problems: list[Problem] = []
        self.overlaps: list[OverlapData] = []

    def report_problems(self):
        self.find_overlaps()
        for ix, data in enumerate(self.overlaps):
            self.problems.append(
                Problem(ix, ProblemType.OVERLAP, nbs=data.rooms, geometry=data.shape)
            )

    def find_overlaps(self):
        assert self.G
        for edge in self.G.edges:
            u, v = edge
            if self.shapes[u].overlaps(self.shapes[v]):
                geometry = intersection(self.shapes[u], self.shapes[v])
                assert isinstance(geometry, Polygon)
                p = OverlapData(
                    geometry,
                    edge,
                )
                self.overlaps.append(p)
