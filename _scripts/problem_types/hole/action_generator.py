from shapely import STRtree, Point

from svg_helpers.layout import Layout
from svg_helpers.layout_base import LayoutBase
from problems.classes.problem import Problem, ProblemType
from problems.classes.actions import Action, ActionType

from problem_types.action_abc import ActionBase

from svg_helpers.shapely import  shape_to_decimal_corners
from svg_helpers.helpers import key_from_value
from svg_helpers.decimal_operations import decimal_sub


class HoleActionGenerator(ActionBase):
    def __init__(self, problem: Problem, layout: Layout) -> None:
        super().__init__(problem, layout)
        # self.problem = problem
        assert self.problem.problem_type == ProblemType.HOLE

    def generate_action(self):
        self.action_type = ActionType.STRETCH
        self.determine_direction()
        if self.general_direction:
            self.determine_distance()
            self.determine_node()
            assert self.node and self.distance
            self.action = Action(
                self.problem, self.action_type, self.node, self.distance
            )

    def determine_direction(self):
        self.general_direction = True

    def determine_distance(self):
        assert self.problem.geometry
        c = shape_to_decimal_corners(self.problem.geometry)
        self.distance = abs(c.x_right - c.x_left)

    def determine_node(self):
        self.tree = STRtree(list(self.shapes.values()))
        assert self.problem.geometry
        x = bounds_to_corners(self.problem.geometry.bounds).x_left
        y = self.problem.geometry.centroid.y
        ix = self.tree.nearest(Point(x, y))
        nearest = self.tree.geometries.take(ix)
        self.node = key_from_value(self.shapes, nearest)
