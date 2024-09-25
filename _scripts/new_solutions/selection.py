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
from visuals.plotter import plot_general
from svg_logger.settings import svlogger

# select problems


# ----
T = TypeVar("T")


def sort_and_group_objects(lst: List[T], fx: Callable[[T], Any]) -> List[List[T]]:
    sorted_objs = sorted(lst, key=fx)
    return [list(g) for _, g in groupby(sorted_objs, fx)]


def calculate_size_of_problems(problems: list[Problem]) -> float:
    return reduce(add, map(lambda x: x.geometry.area, problems))


def sort_results_by_size_of_problem_geometry(results: List[ResultsLog]):
    return sorted(results, key=lambda x: calculate_size_of_problems(x.problems))


def flatten_sorted_groups(sorted_groups: List[List[ResultsLog]]) -> list[ResultsLog]:
    return [item for sublist in sorted_groups for item in sublist]


def sort_results(results: List[ResultsLog]) -> List[ResultsLog]:
    grouped_res = sort_and_group_objects(results, lambda x: x.num_unresolved_problems)
    sorted_groups = [sort_results_by_size_of_problem_geometry(g) for g in grouped_res]
    return flatten_sorted_groups(sorted_groups)


def get_next_best_result(
    current_result: ResultsLog, sorted_results: List[ResultsLog]
) -> ResultsLog:
    ix = sorted_results.index(current_result) + 1
    try:
        return sorted_results[ix]
    except IndexError:
        raise Exception("No more results!")


def is_corner_overlap(a: Domain, b: Domain) -> bool:
    cmp = a.compare_domains(
        b, consider_overlap=True
    )  # TODO move this to domains.. , see if relationship to withiness
    if cmp.is_empty():
        cmp = b.compare_domains(a, consider_overlap=True)
    directions = cmp.get_domain_directions(a)
    if len(directions) > 1:
        return True
    return False


def is_corner_overlap_in_result(res: ResultsLog) -> bool:
    overlaps = [p for p in res.new_problems if p.problem_type == ProblemType.OVERLAP]
    for o in overlaps:
        doms = [res.layout.domains[i] for i in o.nbs]
        if is_corner_overlap(*doms):
            return True
    return False


def get_next_best_result_wo_corner_overlap(
    curr: ResultsLog, sorted_res: List[ResultsLog]
):
    print("helloo!")
    cnt = 0
    while sorted_res:
        # svlogger.debug(f"prob at ix {cnt}")
        if is_corner_overlap_in_result(curr):
            print(f"skipping bc of corner overlap {cnt}")
            curr = get_next_best_result(curr, sorted_res)
            cnt += 1
        else:
            return get_next_best_result(curr, sorted_res)
    raise Exception("No results without corner overlaps!")


# pr = ProblemResults(sop.problem, sop.layout, flattened_groups[:10] )
# make_subplot_for_results(pr)
# --------


def init_let_it_cook(init_report: Reporter, filter_desc: FilterDesc):
    sop = StudyOneProblem(*init_report.output, filter_desc)
    print(f"Initial Problems: {init_report.summary}")
    plot_general(init_report.layout.domains)
    sop.run()
    sorted_res = sort_results(sop.results)
    bl = get_next_best_result_wo_corner_overlap(sorted_res[0], sorted_res)
    output = (bl.layout, bl.summary, bl.problems)
    print(f"First best layout: {bl}")
    return output


def let_it_cook(output: tuple[Layout, Counter[str], list[Problem]]):
    sop = StudyOneProblem(*output)  # choosing the one with the smallest x
    sop.run()
    sorted_res = sort_results(sop.results)
    bl = get_next_best_result_wo_corner_overlap(sorted_res[0], sorted_res)
    print(f"Next best layout: {bl}")
    output = (bl.layout, bl.summary, bl.problems)

    return output


# report = run_new_layout()
# output = init_let_it_cook(report, FilterDesc(ProblemType.HOLE, []))

# output2 = let_it_cook(output1)
# plot_general(output[0].domains)


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


def init_let_all_cook(init_report: Reporter):
    history = []
    print(f"First run. Problems are {init_report.summary}")
    history.append(init_report.layout.domains)
    results = study_many_problems(*init_report.output)

    return repeated(results), history


def let_all_cook(output, history: list):
    results = study_many_problems(*output)
    bl, output, sorted_res = repeated(results)
    print(bl)
    while is_domain_in_history(bl.layout.domains, history):
        bl = get_next_best_result_wo_corner_overlap(bl, sorted_res)
        print(f"prev domains are in history - next best layout: {bl}")
        output = (bl.layout, bl.summary, bl.problems)
    history.append(bl.layout.domains)
    return bl, output, sorted_res, history


def repeated(results):
    sorted_res = sort_results(results)
    bl = get_next_best_result_wo_corner_overlap(sorted_res[0], sorted_res)
    print(f"Next best layout: {bl}")
    output = (bl.layout, bl.summary, bl.problems)
    return bl, output, sorted_res

    # history.append(bl.layout.domains)


class Cook:
    def __init__(self, init_report: Reporter) -> None:
        self.history = []
        self.res_hist = []
        self.bl_hist = []
        self.history.append(init_report.layout.domains)
        self.results = study_many_problems(*init_report.output)
        
        self.handle()
        self.count = 0
        print(self.count)

    def run_again(self):
        self.count+=1
        print(f"running again -> {self.count}")
        self.results = study_many_problems(
            self.bl.layout, self.bl.summary, self.bl.problems
        )
        self.handle()

    def handle(self):
        self.sorted_res = sort_results(self.results)
        self.res_hist.append(self.sorted_res)
        self.bl = get_next_best_result_wo_corner_overlap(self.sorted_res[0], self.sorted_res)
        print(f"first bl to try -> {self.bl}")
        while is_domain_in_history(self.bl.layout.domains, self.history):
            self.bl = get_next_best_result_wo_corner_overlap(self.bl, self.sorted_res)
            print(f"prev domains are in history - next best layout: {self.bl}")
        print(f"problem this fixes -> {self.bl.problem_being_addressed}")
        self.history.append(self.bl.layout.domains)
        self.bl_hist.append(self.bl)

    def plot(self, ix):
        plot_general(self.history[ix])

