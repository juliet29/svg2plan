from copy import deepcopy
from typing import Counter, List, Optional
from actions.actions import CreateModifiedDomain
from actions.results_log import ResultsLog
from identify.reporter import Reporter
from helpers.shapely import domain_to_shape
from actions.interfaces import ActionDetails
from helpers.layout import Layout
from identify.interfaces import Problem
from actions.interfaces import OperationLog
from svg_logger.settings import svlogger


def create_node_operations(action_details: ActionDetails):
    operations: list[OperationLog] = []
    for action_type in action_details.action_types:
        cmd = CreateModifiedDomain(action_details, action_type)
        op = cmd.create_domain()
        if op is not None:
            operations.append(op)

    return operations


def execute_actions(problem: Problem):
    operations: list[OperationLog] = []
    for details in problem.action_details:
        operations.extend(create_node_operations(details))
    return operations


def update_layout(op: OperationLog, layout: Layout):
    name = op.node.name
    tmp_layout: Layout = deepcopy(layout)
    tmp_layout.domains[name] = op.modified_domain
    return tmp_layout


def report_on_actions(
    op: OperationLog,
    problem: Problem,
    tmp_layout: Layout,
    initial_problems: list[Problem] = [],
):
    try:
        re = Reporter(tmp_layout, initial_problems)
        re.run()
        return ResultsLog(op, re.summary, re.problems, re.new, tmp_layout, problem)
    except AssertionError:
        print(f"Could not report on problems for {op.action_type} on {op.node.name}")
        return None


def study_one_problem(layout, problem, initial_problems: list[Problem] = []):
    ops = execute_actions(problem)

    def update_and_report(op: OperationLog):
        tmp_layout = update_layout(op, layout)
        return report_on_actions(op, problem, tmp_layout, initial_problems)

    return [update_and_report(i) for i in ops]


def study_many_problems(layout: Layout, problems: List[Problem]) -> list[ResultsLog]:
    results: list[ResultsLog] = []
    valid_probs = [p for p in problems if p.resolved == False]
    for curr_prob in valid_probs:
        s = study_one_problem(layout, curr_prob, valid_probs)
        results.extend(list(filter(None, s)))
    return results
