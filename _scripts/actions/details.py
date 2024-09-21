from svg_helpers.directions import Direction, get_axis
from new_corners.domain import Domain
from decimal import Decimal
from actions.interfaces import CurrentDomains
from log_setter.log_settings import logger


class Details:
    def __init__(self, current_domains: CurrentDomains) -> None:
        self.problem = current_domains.problem
        self.node = current_domains.node

        self.problem_size: Decimal
        self.relative_direction: Direction
        self.run()

    def run(self):
        self.get_direction_relative_to_problem()
        self.get_problem_size()

    def get_direction_relative_to_problem(self):
        self.cmp = self.node.compare_domains(self.problem, consider_overlap=True)
        if self.cmp.is_empty():
            self.cmp = self.problem.compare_domains(self.node, consider_overlap=True)
        if self.cmp.is_empty():
            raise Exception("Invalid relationship between domains")

        directions = self.cmp.get_domain_directions(self.node)
        self.relative_directions = [Direction[i] for i in directions]
        # if len(directions) > 1:
        #     logger.warning(f"Too many directions for {self.node.name}: {directions}") # TODO try both directions later.. 
        # direction = self.cmp.get_domain_directions(self.node)[0]

    def get_problem_size(self):
        axis = get_axis(self.relative_direction)
        match axis:
            case "y":
                self.problem_size = self.problem.y.size
            case "x":
                self.problem_size = self.problem.x.size
            case _:
                raise Exception("Invalid axis")
