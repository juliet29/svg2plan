from typing import Dict
from dataclasses import dataclass
from networkx import Graph
from shapely import Polygon, intersection, union_all, STRtree, LinearRing
from problems.classes.problem import Problem, ProblemType
from classes.layout import Layout
from svg_helpers.helpers import key_from_value
from copy import deepcopy




class Reporter:
    def __init__(
        self,
        layout: Layout,
        existing_problems: list[Problem] = [],
    ) -> None:
        self.shapes = deepcopy(layout.shapes)
        self.G = deepcopy(layout.graph)
        self.corners = deepcopy(layout.corners)
        self.problems: list[Problem] = deepcopy(existing_problems)
        self.index = len(self.problems)
        self.candidates = []

    def run(self):
        self.reset_exisiting_problems()
        self.find_overlaps()
        self.find_holes()
        self.check_for_resolved()
        self.summarize()

    def reset_exisiting_problems(self):
        for p in self.problems:
            p.matched = False


    def find_overlaps(self):
        assert self.G
        for edge in self.G.edges:
            u, v = edge
            if self.shapes[u].overlaps(self.shapes[v]):
                geometry = intersection(self.shapes[u], self.shapes[v])
                assert isinstance(geometry, Polygon)
                self.candidate_problem = Problem(
                    self.index,
                    ProblemType.OVERLAP,
                    edge,
                    geometry,
                )
                self.compare_with_existing()

    def find_holes(self):
        self.union = union_all(list(self.shapes.values()))
        assert isinstance(self.union, Polygon)

        self.tree = STRtree(list(self.shapes.values()))
        for hole in self.union.interiors:
            assert isinstance(hole, LinearRing)
            self.candidate_problem = Problem(
                self.index,
                ProblemType.HOLE,
                self.find_rooms_surrounding_hole(),
                Polygon(hole),
            )
            self.compare_with_existing()


    def compare_with_existing(self):
        self.candidates.append(self.candidate_problem)
        for p in self.problems:
            if self.candidate_problem == p:
                p.matched = True
                return
        self.add_problem_and_update_index()


    def add_problem_and_update_index(self):
        self.problems.append(self.candidate_problem)
        self.index += 1
        self.compare_with_existing()

    def check_for_resolved(self):
        for p in self.problems:
            if p.matched == False:
                p.resolved = True



    def find_rooms_surrounding_hole(self):
        assert isinstance(self.union, Polygon)
        indices = self.tree.query_nearest(self.union.interiors[0])
        nearest = self.tree.geometries.take(indices).tolist()
        rooms = [key_from_value(self.shapes, p) for p in nearest]
        return rooms

    def summarize(self):
        self.overlaps = [
            p for p in self.problems if p.problem_type == ProblemType.OVERLAP and p.resolved == False
        ]
        self.holes = [p for p in self.problems if p.problem_type == ProblemType.HOLE and p.resolved == False]
        print(f"Overlaps: {len(self.overlaps)}. Holes: {len(self.holes)}.")
        
