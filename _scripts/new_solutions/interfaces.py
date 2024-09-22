# svlogger.info(f"problem nbs: {problem.nbs}")


from actions.interfaces import OperationLog
from new_corners.domain import Domain
from problems.classes.problem import Problem


from dataclasses import dataclass
from typing import Dict


@dataclass
class ResultsLog:
    operations: OperationLog
    results: str  # Reporter.txt
    problems: list[Problem]
    domains: Dict[str, Domain]

    @property
    def num_unresolved_problems(self):
        return len([i for i in self.problems if not i.resolved])

    def __repr__(self) -> str:
        return f"node: {self.operations.node.name}, action: {self.operations.action_type.name}, results: {self.results}, # unres probs: {self.num_unresolved_problems}"
