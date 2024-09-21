from typing import Dict
from new_corners.domain import Domain
from new_corners.range import Range, InvalidRangeException
from svg_helpers.domains import DecimalCorners
from svg_helpers.saver import read_layout
from problems.classes.problem import Problem, ProblemType
from svg_helpers.shapely import shape_to_decimal_corners
from actions.actions import ExecuteAction
from actions.interfaces import ActionType
from actions.interfaces import CurrentDomains
from log_setter.log_settings import logger
from dataclasses import dataclass



@dataclass
class OperationLogger:
    node: Domain
    action_type: ActionType
    modified_domain: Domain | None

layout = read_layout("amber_a_placed")
problem: Problem
# [problem]= [i for i in layout.problems if i.problem_type == ProblemType.HOLE]
problem = layout.problems[0]
prob_name = "problem"
logger.info(f"problem nbs: {problem.nbs}")


def corner_to_domain(name: str, corner: DecimalCorners):
    x_range = Range(corner.x_left, corner.x_right)
    y_range = Range(corner.y_bottom, corner.y_top)
    return Domain(name, x_range, y_range)


def create_domains():
    domains: Dict[str, Domain] = {}
    for name, corner in layout.corners.items():
        domains[name] = corner_to_domain(name, corner)
    assert problem.geometry
    problem_corner = shape_to_decimal_corners(problem.geometry)
    domains[prob_name] = corner_to_domain(prob_name, problem_corner)

    return domains


def execute_actions():
    domains = create_domains()
    operations: list[OperationLogger] = []
    for name in problem.nbs:
        node = domains[name]
        prob = domains[prob_name]
        logger.info(f"current node: {name}")
        for action in ActionType:
            try:
                ea = ExecuteAction(CurrentDomains(node, prob), action)
                res = ea.modified_domain
            except InvalidRangeException:
                logger.warning(
                    f"{action.name} operation on {node.name} produced invalid range"
                )
                res = None

            operations.append(OperationLogger(node, action, res))

    return operations
    
# operations = execute_actions()


