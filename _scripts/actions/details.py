from svg_helpers.directions import Direction, get_axis
from new_corners.domain import Domain
from decimal import Decimal
from actions.interfaces import CurrentDomains

class Details:
    def __init__(self, current_domains: CurrentDomains) -> None:
        self.problem = current_domains.problem
        self.node = current_domains.node

        self.problem_size: Decimal
        self.direction_relative_to_problem: Direction
        # self.action_direction:  Direction

    def run(self):
        self.get_direction_relative_to_problem()
        self.get_problem_size()


    def get_direction_relative_to_problem(self):
        self.cmp = self.problem.compare_domains(self.node)
        direction = self.cmp.get_key_from_domain(self.node)
        self.direction_relative_to_problem = Direction[direction]

    
    def get_problem_size(self):
        axis = get_axis(self.direction_relative_to_problem)
        match axis:
            case "y":
                self.problem_size = self.problem.y.size
            case "x":
                self.problem_size = self.problem.x.size
            case _:
                raise Exception("Invalid axis")

