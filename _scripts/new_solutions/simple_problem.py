from copy import deepcopy
from os import name
from typing import Callable, Counter, List, Optional
from actions.actions import create_node_operations
from new_solutions.interfaces import ResultsLog, ProblemResults
from helpers.layout import Layout
from visuals.plots import make_subplot_for_results
from export.saver import read_layout
from fixes.interfaces import Problem, ProblemType
from actions.interfaces import OperationLog
from actions.interfaces import CurrentDomains
from svg_logger.settings import svlogger
from visuals.plotter import Plotter
from plotly.subplots import make_subplots
from collections import namedtuple


from fixes.reporter import Reporter

from helpers.shapely import domain_to_shape, shape_to_domain



# layout = read_layout("amber_a_placed")
# problem: Problem
# # [problem] = [i for i in layout.problems if i.problem_type == ProblemType.HOLE]
# problem = layout.problems[3]
# prob_name = "problem"

def compare_nbs(nbs: List[str], nbs_to_find: List[str]):
    if nbs_to_find == []:
        return True
    for n in nbs:
        if n in nbs_to_find:
            return True
    return False

def filter_problems(problems: List[Problem], type: ProblemType, nbs: List[str]):
    fx: Callable[[Problem], bool] = lambda p : p.problem_type == type and compare_nbs(p.nbs, nbs)
    return list(filter(fx, problems))[0]

description = tuple[Layout, Counter[str], list[Problem]]
FilterDesc = namedtuple("FilterDesc", ["problem_type", "nbs"])

def select_next_problem_by_x(problems: list[Problem]):
    return sorted(problems,  key=lambda x: x.geometry.bounds[0])[0]

class StudyOneProblem:
    def __init__(self, layout: Layout, summary: Counter, problems: List[Problem], filter_desc: Optional[FilterDesc] = None) -> None:
        self.layout = layout
        self.init_problems = problems
        if filter_desc:
            self.problem = filter_problems(problems, *filter_desc)
        else:
            self.problem = select_next_problem_by_x(problems)
        self.init_summary = summary


    def run(self):
        ops = self.execute_actions()
        self.results = list(filter(None, [self.study_operation(i) for i in ops]))
        self.problem_results = ProblemResults(self.problem, self.layout, self.results)
        # make_subplot_for_results(p)


    def execute_actions(self):
        domains = self.layout.domains
        operations: list[OperationLog] = []
        for name in self.problem.nbs:
            svlogger.info(f"studying operations for node: {name}")
            node = domains[name]
            assert self.problem.geometry
            prob = shape_to_domain(self.problem.geometry, "problem")
            operations.extend(create_node_operations(CurrentDomains(node, prob)))

        return operations


    def study_operation(self, op: OperationLog):
        name = op.node.name
        tmp_layout: Layout = deepcopy(self.layout)

        if op.modified_domain:
            tmp_layout.domains[name] = op.modified_domain
            tmp_layout.shapes[name] = domain_to_shape(op.modified_domain)
        try:
            re = Reporter(tmp_layout, self.init_problems)
            re.run()
            return ResultsLog(op, re.summary, re.problems, re.new, tmp_layout)
        except AssertionError:
            svlogger.warning(f"Could not report on problems for {op.action_type} on {op.node.name}")
            pass




# def plot_index(results: list[ResultsLog], ix: int):
#     plt = Plotter(results[ix].domains)
#     plt.plot()


# def plot_results(report: Reporter):
#     p = StudyOneProblem(report, ProblemType.HOLE, ['transit_space', 'laundry'])
#     p.run()
#     fig = make_subplot_for_results(p.results)

#     fig.show()

#     return fig


# def run():
    # res = conduct_study()
    # good_res = [i for i in res if i and i.num_unresolved_problems <= 3]
    # plot_results(good_res)
    # print("num res:", len(res))
    # print("prob count:", [i.num_unresolved_problems for i in res if i])

    # return res, good_res


# operations = execute_actions()
