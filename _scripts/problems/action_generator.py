from shapely import STRtree, Point
from copy import deepcopy

from classes.layout import Layout
from classes.directions import Direction, DIRECTION_PAIRS

from problems.classes.problem import Problem, ProblemType
from problems.classes.actions import Action, ActionType
from problems.classes.sequence import Sequence
from problems.classes.problems_base import ProblemsBase

from svg_helpers.shapely import bounds_to_corners
from svg_helpers.helpers import key_from_value


class ActionGenerator(ProblemsBase):
    def __init__(self, problem: Problem, layout: Layout) -> None:
        super().__init__(deepcopy(layout))
        self.problem = problem
        # TODO redundant with reporter.py
        self.tree = STRtree(list(layout.shapes.values()))
        # self.shapes = layout.shapes
        # self.G = layout.G

    def generate_action(self):
        self.determine_distance()
        self.determine_node_and_type()
        self.action = Action(self.problem, self.action_type, self.node, self.distance)
        print(self.action)
        return self.action

    def determine_distance(self):
        c = bounds_to_corners(self.problem.geometry.bounds)
        self.distance = c.x_right - c.x_left

    def determine_node_and_type(self):
        match self.problem.problem_type:
            case ProblemType.OVERLAP:
                assert len(self.problem.nbs) == 2
                self.get_node_in_direction_of_overlap()
                self.action_type = ActionType.PUSH
            case ProblemType.HOLE:
                assert len(self.problem.nbs) == 4
                self.get_node_left_of_hole()
                self.action_type = ActionType.STRETCH
            case _:
                raise (Exception("Invalid problem type"))

    def get_node_left_of_hole(self):
        x = bounds_to_corners(self.problem.geometry.bounds).x_left
        y = self.problem.geometry.centroid.y
        ix = self.tree.nearest(Point(x, y))
        nearest = self.tree.geometries.take(ix)
        self.node = key_from_value(self.shapes, nearest)

    def get_node_in_direction_of_overlap(self):
        self.u, self.v = self.problem.nbs
        if self.is_overlap_dir(Direction.EAST):
            return
        elif self.is_overlap_dir(Direction.NORTH):
            return

    def is_overlap_dir(self, dir: Direction):
        assert self.G
        if self.v in self.G.nodes[self.u]["data"][dir.name]:
            # print(f"{self.v} is the {dir.name} node")
            self.node = self.v
            return True
        elif self.v in self.G.nodes[self.u]["data"][DIRECTION_PAIRS[dir].name]:
            # print(f"{self.u} is the {dir.name} node")
            self.node = self.u
            return True
        else:
            return False
