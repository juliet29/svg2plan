from svg_helpers.layout import Layout
from svg_helpers.directions import (
    GeneralDirection,
    DirectedPairEW,
    DirectedPairNS,
    make_directed_pair,
)
from problem_types.action_abc import ActionBase
from svg_helpers.layout_base import LayoutBase
from problems.classes.problem import Problem, ProblemType
from problems.classes.actions import Action, ActionType



class SideHoleActionGenerator(ActionBase):
    def __init__(self, problem: Problem, layout: Layout) -> None:
        super().__init__(problem, layout)
        assert self.problem.problem_type == ProblemType.SIDE_HOLE

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
        u, v = self.problem.nbs
        try:
            [self.d] = make_directed_pair(self.G, u, v)
        except ValueError:
            print("More than one directed pair")
            return

        if isinstance(self.d, DirectedPairEW):
            self.general_direction = GeneralDirection.EAST_WEST
        elif isinstance(self.d, DirectedPairNS):
            print("NS directed pair not implemented")
            return

    def determine_distance(self):
        match self.general_direction:
            case GeneralDirection.EAST_WEST:
                self.distance = (
                    self.corners[self.d.EAST].x_left - self.corners[self.d.WEST].x_right
                )
            case _:
                self.distance = None

    def determine_node(self):
        match self.general_direction:
            case GeneralDirection.EAST_WEST:
                self.node = self.d.WEST
            case _:
                self.node = None
