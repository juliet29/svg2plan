from decimal import Decimal
from functools import reduce
from itertools import groupby
from operator import add
from typing import Any, Callable, Dict, List, TypeVar

from matplotlib.pyplot import hist
from domains.domain import Domain
from fixes.interfaces import Problem, ProblemType
from fixes.reporter import Reporter
from helpers.layout import Layout
from new_solutions.interfaces import ResultsLog
from collections import Counter, namedtuple

from new_solutions.simple_problem import (
    FilterDesc,
    StudyOneProblem,
    study_many_problems,
)
from visuals.plots import make_subplot_for_all_probs
from visuals.plotter import plot_general
from svg_logger.settings import svlogger


T = TypeVar("T")


def sort_and_group_objects(lst: List[T], fx: Callable[[T], Any]) -> List[List[T]]:
    sorted_objs = sorted(lst, key=fx)
    return [list(g) for _, g in groupby(sorted_objs, fx)]



def sort_results_by_score(results: List[ResultsLog]):
    return sorted(results, key=lambda x: x.score)


# def flatten_sorted_groups(sorted_groups: List[List[ResultsLog]]) -> list[ResultsLog]:
#     return [item for sublist in sorted_groups for item in sublist]


# def sort_results(results: List[ResultsLog]) -> List[ResultsLog]:
#     grouped_res = sort_and_group_objects(results, lambda x: x.num_unresolved_problems)
#     sorted_groups = [sort_results_by_size_of_problem_geometry(g) for g in grouped_res]
#     return flatten_sorted_groups(sorted_groups)


def get_next_best_result(
    current_result: ResultsLog, sorted_results: List[ResultsLog]
) -> ResultsLog:
    ix = sorted_results.index(current_result) + 1
    try:
        return sorted_results[ix]
    except IndexError:
        raise Exception("No more results!")


def are_domains_equal(doms_a, doms_b):
    try:
        assert len(doms_a) == len(doms_b)
        for key in doms_a:
            try:
                assert doms_a[key] == doms_b[key]
            except:
                # print(f"{key} doesnt match - doms are not equal")
                return False
    except AssertionError as e:
        print("Unequal len")
        return False
    return True


def is_domain_in_history(curr_dom, hist: list):
    for h in hist:
        if are_domains_equal(h, curr_dom):
            return True


class Cook:
    def __init__(self, init_report: Reporter) -> None:
        self.res_hist = []
        self.bl_hist = []
        self.history = [init_report.layout.domains]
        self.results = study_many_problems(*init_report.output)
        
        self.count = 0
        print(f"initializing.. {self.count}")
        self.handle()

    def run_again(self):
        self.results = study_many_problems(
            self.bl.layout, self.bl.summary, self.bl.problems
        )
        self.handle()
        print(f"running again -> {self.count}")

    def handle(self):
        self.count+=1
        self.sorted_res = sort_results_by_score(self.results)
        self.res_hist.append(self.sorted_res)
        self.bl = get_next_best_result(self.sorted_res[0], self.sorted_res)
        print(f"problem being studied: -> {self.bl.problem_being_addressed}")
        print(f"first bl to try -> {self.bl}")
        while is_domain_in_history(self.bl.layout.domains, self.history):
            self.bl = get_next_best_result(self.bl, self.sorted_res)
            print(f"skipping bc prev domains are in history")
        print(f"next best layout {self.bl}")
        self.history.append(self.bl.layout.domains)
        self.bl_hist.append(self.bl)

    def plot(self, ix):
        plot_general(self.history[ix], f"iteration {ix}")

    def plot_all(self):
        make_subplot_for_all_probs(self.history[0], self.bl_hist)

    def show_results_at_ix(self, ix):
        [i.short_message() for i in self.res_hist[ix]]


