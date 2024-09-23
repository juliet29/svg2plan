from helpers.directions import Direction, get_axis
from new_corners.domain import Domain
from decimal import Decimal
from actions.interfaces import CurrentDomains
from svg_logger.settings import svlogger


class Details:
    def __init__(self, current_domains: CurrentDomains) -> None:
        self.problem = current_domains.problem
        self.node = current_domains.node
        self.problem_sizes: list[Decimal] = []

    def run(self):
        self.get_directions_relative_to_problem()
        self.gather_problem_sizes()
        self.result = list(zip(self.problem_sizes, self.relative_directions))

    def get_directions_relative_to_problem(self):
        self.cmp = self.node.compare_domains(self.problem, consider_overlap=True)
        if self.cmp.is_empty():
            self.cmp = self.problem.compare_domains(self.node, consider_overlap=True)
        if self.cmp.is_empty():
            raise Exception("Invalid relationship between domains")

        directions = self.cmp.get_domain_directions(self.node)
        self.relative_directions = [Direction[i] for i in directions]

    def gather_problem_sizes(self):
        for drn in self.relative_directions:
            axis = get_axis(drn)
            self.problem_sizes.append(self.get_problem_size(axis))

    def get_problem_size(self, axis):
        match axis:
            case "y":
                return self.problem.y.size
            case "x":
                return self.problem.x.size
            case _:
                raise Exception("Invalid axis")
