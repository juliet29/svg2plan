from collections import Counter, namedtuple
from copy import deepcopy
from icecream import ic

from helpers.layout import Layout
from fixes.interfaces import Problem, ProblemType
from fixes.interfaces import LayoutBase

from fixes.problem_types.overlap_id import create_overlap_problems
from fixes.problem_types.hole_id import create_hole_problems
from fixes.problem_types.side_hole_id import create_side_hole_problems
from svg_logger.settings import svlogger


class Reporter:
    def __init__(self, layout: Layout, existing_problems: list[Problem] = []) -> None:
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

        self.output = (self.layout, self.summary, self.problems)

    def find_new(self):
        for identifier in [create_side_hole_problems, create_overlap_problems, create_hole_problems]:
            probs = identifier(self.layout)
            if probs:
                self.candidates.extend(probs)

    def compare_new_and_old(self):
        new_probs = set(self.candidates)
        old_probs = set(self.problems)

        self.old_not_resolved = old_probs.intersection(new_probs)
        self.old_resolved = old_probs.difference(new_probs)
        self.new = list(new_probs.difference(old_probs))

    def handle_resolved(self):
        for p in self.old_resolved:
            p.resolved = True

    def update_indices_of_new(self):
        for p in self.new:
            self.index += 1
            p.index = self.index

    def merge_new_and_old(self):
        self.problems.extend(self.new)

    def summarize(self):
        self.summary = Counter([i.problem_type.name for i in self.problems if i.resolved == False])
