from copy import deepcopy
from typing import Dict
from new_corners.domain import Domain
from actions.actions import create_node_operations
from svg_helpers.layout import Layout
from svg_helpers.saver import read_layout
from problems.classes.problem import Problem, ProblemType
from actions.interfaces import OperationLog
from actions.interfaces import CurrentDomains
from log_setter.log_settings import svlogger
from dataclasses import dataclass
from svg_helpers.plotter import Plotter
from plotly.subplots import make_subplots

from problems.reporter import Reporter

from svg_helpers.shapely import domain_to_shape, shape_to_domain


layout = read_layout("amber_a_placed")
problem: Problem
[problem] = [i for i in layout.problems if i.problem_type == ProblemType.HOLE]
problem = layout.problems[1]
prob_name = "problem"
# svlogger.info(f"problem nbs: {problem.nbs}")


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


def execute_actions():
    domains = layout.domains
    operations: list[OperationLog] = []
    for name in problem.nbs:
        svlogger.info(f"studying operations for node: {name}")
        node = domains[name]
        assert problem.geometry
        prob = shape_to_domain(problem.geometry, "problem")
        operations.extend(create_node_operations(CurrentDomains(node, prob)))

    return operations


def study_operation(op: OperationLog):
    # make a copy of layout
    name = op.node.name
    tmp_layout: Layout = deepcopy(layout)

    if op.modified_domain:
        tmp_layout.domains[name] = op.modified_domain
        tmp_layout.shapes[name] = domain_to_shape(op.modified_domain)

    try:
        re = Reporter(tmp_layout)
        re.run()
        return ResultsLog(op, re.txt, re.problems, tmp_layout.domains)
    except AssertionError as e:
        print(f"Maybe a problem with finding holes when doing a {op.action_type.name} on {name}")
        return None



def conduct_study():
    ops = execute_actions()
    return [study_operation(i) for i in ops]

def plot_index(results: list[ResultsLog], ix:int):
    plt = Plotter(results[ix].domains)
    plt.plot()


def plot_results(results: list[ResultsLog]):
    pass



# operations = execute_actions()
