from classes.layout import Layout
from classes.directions import Direction
from problems.classes.problems_base import ProblemsBase
from shapely import Polygon, intersection
from problems.classes.problem import Problem, ProblemType

class OverlapIdentifier(ProblemsBase):
    def __init__(self, layout:Layout) -> None:
        super().__init__(layout)
        self.problems = []

    def find_overlaps(self):
        assert self.G
        for ix, edge in enumerate(self.G.edges):
            u, v = edge
            if self.shapes[u].overlaps(self.shapes[v]):
                geometry = intersection(self.shapes[u], self.shapes[v])
                assert isinstance(geometry, Polygon)
                p = Problem(
                    ix,
                    ProblemType.OVERLAP,
                    edge,
                    geometry,
                )
                self.problems.append(p)