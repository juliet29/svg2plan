from dataclasses import dataclass
from new_corners.domain import Domain

@dataclass
class CurrentDomains:
    node: Domain
    problem: Domain