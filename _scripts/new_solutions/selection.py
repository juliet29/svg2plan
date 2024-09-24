from decimal import Decimal
from functools import reduce
from itertools import groupby
from operator import add
from typing import Any, Callable, Dict, List, TypeVar
from domains.domain import Domain
from fixes.interfaces import Problem, ProblemType
from fixes.reporter import Reporter
from helpers.layout import Layout
from new_solutions.interfaces import ResultsLog
from collections import Counter, namedtuple

from new_solutions.simple_problem import FilterDesc, StudyOneProblem
from visuals.plotter import plot_general

# select problems




    
# ----
T = TypeVar("T")
def sort_and_group_objects(lst: List[T], fx: Callable[[T], Any]) -> List[List[T]]:
    sorted_objs = sorted(lst, key=fx)
    return [list(g) for _,g in groupby(sorted_objs, fx)]

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




def get_next_best_result(current_result:ResultsLog, sorted_results: List[ResultsLog]) -> ResultsLog:
    ix = sorted_results.index(current_result) + 1
    try:
        return sorted_results[ix]
    except IndexError:
        raise Exception("No more results!")


def is_corner_overlap(a: Domain, b:Domain) -> bool:
    cmp = a.compare_domains(b, consider_overlap=True) # TODO move this to domains.. , see if relationship to withiness
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

def get_next_best_result_wo_corner_overlap(curr, sorted_res):
    while sorted_res:
        if is_corner_overlap_in_result(curr):
            curr = get_next_best_result(curr, sorted_res)
        else:
            return curr
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
    sop = StudyOneProblem(*output) # choosing the one with the smallest x  
    sop.run()
    sorted_res = sort_results(sop.results)
    bl = get_next_best_result_wo_corner_overlap(sorted_res[0], sorted_res)
    print(f"Next best layout: {bl}")
    output = (bl.layout, bl.summary, bl.problems)

    return output


# report = run_new_layout()
# output = init_let_it_cook(report, FilterDesc(ProblemType.HOLE, []))
