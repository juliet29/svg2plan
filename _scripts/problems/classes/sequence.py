from dataclasses import dataclass, field
from typing import Dict
from svg_helpers.layout import Layout
from problems.classes.problem import Problem
from problems.classes.actions import Action

@dataclass
class Sequence:
    index: int
    layout: Layout
    problems: list[Problem]
    actions: list[Action] = field(default_factory=list)

