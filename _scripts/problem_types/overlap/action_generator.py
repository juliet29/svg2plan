from svg_helpers.layout import Layout
from svg_helpers.directions import GeneralDirection, make_directed_pair
from problem_types.action_abc import ActionBase
from problems.classes.problem import Problem, ProblemType
from problems.classes.actions import Action, ActionType
from svg_helpers.decimal_operations import decimal_sub




class OverlapActionGenerator(ActionBase):
    def __init__(self, problem: Problem, layout: Layout) -> None:
        super().__init__(problem, layout)
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
        c = shape_to_decimal_corners(self.problem.geometry)
        self.distance = abs(c.x_right - c.x_left)


    def determine_node(self):
        if self.general_direction == GeneralDirection.EAST_WEST:
            self.node = self.d.EAST
        elif self.general_direction == GeneralDirection.NORTH_SOUTH:
            self.node = self.d.NORTH

