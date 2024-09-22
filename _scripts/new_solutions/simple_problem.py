from copy import deepcopy
from actions.actions import create_node_operations
from new_solutions.interfaces import ResultsLog
from svg_helpers.layout import Layout
from svg_helpers.plots import make_subplot_for_results
from svg_helpers.saver import read_layout
from problems.classes.problem import Problem, ProblemType
from actions.interfaces import OperationLog
from actions.interfaces import CurrentDomains
from log_setter.log_settings import svlogger
from svg_helpers.plotter import Plotter
from plotly.subplots import make_subplots


from problems.reporter import Reporter

from svg_helpers.shapely import domain_to_shape, shape_to_domain


layout = read_layout("amber_a_placed")
problem: Problem
[problem] = [i for i in layout.problems if i.problem_type == ProblemType.HOLE]
problem = layout.problems[1]
prob_name = "problem"


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
        print(
            f"Maybe a problem with finding holes when doing a {op.action_type.name} on {name}"
        )
        return None


def conduct_study():
    ops = execute_actions()
    return [study_operation(i) for i in ops]


def plot_index(results: list[ResultsLog], ix: int):
    plt = Plotter(results[ix].domains)
    plt.plot()


def plot_results(results: list[ResultsLog]):
    fig = make_subplot_for_results(results)

    fig.show()

    return fig


def run():
    res = conduct_study()
    good_res = [i for i in res if i and i.num_unresolved_problems <=3]
    f = plot_results(good_res)


# operations = execute_actions()
