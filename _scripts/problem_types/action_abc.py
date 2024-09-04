from abc import ABC, abstractmethod
from problems.classes.problems_base import ProblemsBase
from classes.layout import Layout
from problems.classes.problem import Problem, ProblemType
from problems.classes.actions import Action

class ActionBase(ABC, ProblemsBase):
    def __init__(self, problem: Problem, layout: Layout) -> None:
        super().__init__(layout)
        self.problem = problem
        self.action: Action

    @abstractmethod
    def generate_action(self):
        pass

    @abstractmethod
    def determine_direction(self):
        pass

    @abstractmethod
    def determine_distance(self):
        pass

    @abstractmethod
    def determine_node(self):
        pass