from collections import Counter
from dataclasses import dataclass
from decimal import Decimal

from ..helpers.layout import Layout
from ..helpers.utils import chain_flatten
from ..identify.interfaces import Problem
from .interfaces import OperationLog

N_PROBS_WEIGHT = Decimal(0.5)
SIZE_PROBS_WEIGHT = Decimal(0.5)


@dataclass
class ResultsLog:
    operation: OperationLog
    summary: Counter[str]  # Reporter.txt
    problems: list[Problem]
    new_problems: list[Problem]
    layout: Layout
    problem_being_addressed: Problem
    # domains: Dict[str, Domain]

    @property
    def num_unresolved_problems(self):
        return len([i for i in self.problems if not i.resolved])

    @property
    def problem_size(self):
        # some double counting, but will be larger for more complex problems..
        res = chain_flatten([i.action_details for i in self.problems])
        return sum([i.distance for i in res])

    @property
    def score(self):
        return (
            N_PROBS_WEIGHT * self.num_unresolved_problems
            + SIZE_PROBS_WEIGHT * self.problem_size
        )

    def __repr__(self) -> str:
        return f"node: {self.operation.node.name}, action: {self.operation.action_type.name}, summary: {self.summary}, # unres probs: {self.num_unresolved_problems}"

    def short_message(self):
        return f"{self.operation.node.name}-{self.operation.action_type.name}-for-{self.problem_being_addressed.problem_type.name} near {self.problem_being_addressed.nbs[:2]}{self.num_unresolved_problems}-PS:{self.problem_size:.2f}-S:{self.score:.2f}"

    def display_message(self):
        return f"{self.operation.action_type.name} {self.operation.node.name} for {self.problem_being_addressed.problem_type.name} near {self.problem_being_addressed.nbs[:2]} <br> Remaining Problems: {self.num_unresolved_problems} | Problem Size: {self.problem_size:.2f}"
