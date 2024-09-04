from classes.layout import Layout
from classes.directions import GeneralDirection, DirectedPairEW, DirectedPairNS, make_directed_pair
from problems.classes.problems_base import ProblemsBase
from problems.classes.problem import Problem, ProblemType
from problems.classes.actions import Action, ActionType

from svg_helpers.shapely import bounds_to_corners
from svg_helpers.helpers import key_from_value




class OverlapActionGenerator(ProblemsBase):
    def __init__(self, problem: Problem, layout: Layout) -> None:
        super().__init__(layout)
        self.problem = problem
        assert self.problem.problem_type == ProblemType.OVERLAP

    def generate_action(self):
        self.action_type = ActionType.PUSH
        self.determine_direction()
        if self.general_direction:
            self.determine_distance()
            self.determine_node()
            assert self.node and self.distance
            self.action = Action(self.problem, self.action_type, self.node, self.distance)


    def determine_direction(self):
        u,v = self.problem.nbs
        try:
            [self.d] = make_directed_pair(self.G, u,v)
        except ValueError:
            print("More than one directed pair")
            return
        
        if hasattr(self.d, "EAST") and hasattr(self.d, "WEST"):
            self.general_direction = GeneralDirection.EAST_WEST
        elif hasattr(self.d, "NORTH") and hasattr(self.d, "SOUTH"):
            self.general_direction = GeneralDirection.NORTH_SOUTH
            
    def determine_distance(self):
        assert self.problem.geometry
        c = bounds_to_corners(self.problem.geometry.bounds)
        self.distance = c.x_right - c.x_left


    def determine_node(self):
        if self.general_direction == GeneralDirection.EAST_WEST:
            self.node = self.d.WEST
        elif self.general_direction == GeneralDirection.NORTH_SOUTH:
            self.node = self.d.NORTH

