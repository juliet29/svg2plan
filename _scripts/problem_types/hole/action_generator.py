from shapely import STRtree, Point

from classes.layout import Layout
from classes.directions import GeneralDirection, DirectedPairEW, DirectedPairNS, make_directed_pair
from problems.classes.problems_base import ProblemsBase
from problems.classes.problem import Problem, ProblemType
from problems.classes.actions import Action, ActionType

from svg_helpers.shapely import bounds_to_corners
from svg_helpers.helpers import key_from_value




class HoleActionGenerator(ProblemsBase):
    def __init__(self, problem: Problem, layout: Layout) -> None:
        super().__init__(layout)
        self.problem = problem
        assert self.problem.problem_type == ProblemType.OVERLAP

    def generate_action(self):
        self.action_type = ActionType.STRETCH
        self.determine_direction()
        if self.general_direction:
            self.determine_distance()
            self.determine_node()
            assert self.node and self.distance
            self.action = Action(self.problem, self.action_type, self.node, self.distance)


    def determine_direction(self):
        self.general_direction = True

            
    def determine_distance(self):
        assert self.problem.geometry
        c = bounds_to_corners(self.problem.geometry.bounds)
        self.distance = c.x_right - c.x_left



    def determine_node(self):
        self.tree = STRtree(list(self.shapes.values()))
        assert self.problem.geometry
        x = bounds_to_corners(self.problem.geometry.bounds).x_left
        y = self.problem.geometry.centroid.y
        ix = self.tree.nearest(Point(x, y))
        nearest = self.tree.geometries.take(ix)
        self.node = key_from_value(self.shapes, nearest)

