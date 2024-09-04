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

from problem_types.hole.action_generator import HoleActionGenerator
from problem_types.side_hole.action_generator import SideHoleActionGenerator
from problem_types.overlap.action_generator import OverlapActionGenerator
from problem_types.action_abc import ActionBase


class ActionGenerator():
    def __init__(self, problem: Problem, layout: Layout) -> None:
        self.problem = problem
        self.layout = layout

    def handle_case(self):
        self.ag = self.create_action()(self.problem, self.layout)
        self.ag.generate_action()
        self.action = self.ag.action
        
    def create_action(self):
        match self.problem.problem_type:
            case ProblemType.OVERLAP:
                return OverlapActionGenerator
            case ProblemType.HOLE:
                return HoleActionGenerator
            case ProblemType.SIDE_HOLE:
                return SideHoleActionGenerator
            case _:
                raise (Exception("Invalid problem type"))
            

