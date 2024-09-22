from copy import deepcopy
from icecream import ic

from svg_helpers.layout import Layout
from problems.classes.problem import Problem, ProblemType
from svg_helpers.layout_base import LayoutBase

from problem_types.overlap.identifier import OverlapIdentifier
from problem_types.hole.identifier import HoleIdentifier
from problem_types.side_hole.identifier import SideHoleIdentifier
from problems.fix_logger import fix_logger


class Reporter:
    def __init__(
        self,
        layout: Layout,
        existing_problems: list[Problem] = []
    ) -> None:
        self.layout = deepcopy(layout)
        self.problems: list[Problem] = deepcopy(existing_problems)

        self.index = len(self.problems)
        self.candidates: list[Problem] = []

    def run(self):
        self.find_new()
        self.compare_new_and_old()
        self.handle_resolved()
        self.update_indices_of_new()
        self.merge_new_and_old()
        self.summarize()

    def find_new(self):
        for identifier in [OverlapIdentifier, HoleIdentifier, SideHoleIdentifier]:
            self.identifier = identifier(self.layout)
            self.identifier.report_problems()
            self.candidates.extend(self.identifier.problems)

    def compare_new_and_old(self):
        new_probs = set(self.candidates)
        old_probs = set(self.problems)

        self.old_and_unresolved = old_probs.intersection(new_probs)
        self.old_and_resolved = old_probs.difference(new_probs)
        self.new = new_probs.difference(old_probs)

    def handle_resolved(self):
        for p in self.old_and_resolved:
            p.resolved = True

    def update_indices_of_new(self):
        for p in self.new:
            self.index += 1
            p.index = self.index

    def merge_new_and_old(self):
        self.problems.extend(self.new)

    def summarize(self):
        overlap = 0
        hole = 0
        side_hole = 0
        for p in self.problems:
            if p.resolved == False:
                match p.problem_type:
                    case ProblemType.OVERLAP:
                        overlap += 1
                    case ProblemType.HOLE:
                        hole += 1
                    case ProblemType.SIDE_HOLE:
                        side_hole += 1

        self.txt = f"-- Unresolved Problems. Overlaps: {overlap}. Holes: {hole}. Sideholes: {side_hole}"
        fix_logger.debug(
            self.txt
        )
