from collections import Counter
from actions.interfaces import OperationLog
from domains.domain import Domain
from fixes.interfaces import Problem


from dataclasses import dataclass
from typing import Dict

from helpers.layout import Layout


@dataclass
class ResultsLog:
    operations: OperationLog
    summary: Counter[str]  # Reporter.txt
    problems: list[Problem]
    new_problems: list[Problem]
    layout: Layout
    # domains: Dict[str, Domain]

    @property
    def num_unresolved_problems(self):
        return len([i for i in self.problems if not i.resolved])

    def __repr__(self) -> str:
        return f"node: {self.operations.node.name}, action: {self.operations.action_type.name}, summary: {self.summary}, # unres probs: {self.num_unresolved_problems}"

    def short_message(self):
        return f"{self.operations.node.name}-{self.operations.action_type.name}-{self.num_unresolved_problems}"


@dataclass
class ProblemResults:
    problem: Problem
    original_layout: Layout
    results: list[ResultsLog]
