from collections import Counter
from functools import reduce
from operator import add
from actions.interfaces import OperationLog
from domains.domain import Domain
from fixes.interfaces import Problem


from dataclasses import dataclass
from typing import Dict

from helpers.layout import Layout


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
        return reduce(add, map(lambda x: x.geometry.area, self.problems))

    def __repr__(self) -> str:
        return f"node: {self.operation.node.name}, action: {self.operation.action_type.name}, summary: {self.summary}, # unres probs: {self.num_unresolved_problems}"

    def short_message(self):
        return f"{self.operation.node.name}-{self.operation.action_type.name}-for-{self.problem_being_addressed.problem_type.name} near {self.problem_being_addressed.nbs[:2]}{self.num_unresolved_problems}-{self.problem_size:.3f}"


@dataclass
class ProblemResults:
    problem: Problem
    original_layout: Layout
    results: list[ResultsLog]
