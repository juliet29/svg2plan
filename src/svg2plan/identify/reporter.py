from collections import Counter
from copy import deepcopy

from ..helpers.layout import Layout
from .id_problems import report_problems
from .interfaces import Problem


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
        probs = report_problems(self.layout)
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
        self.summary = Counter(
            [i.problem_type.name for i in self.problems if not i.resolved]
        )
