from dataclasses import dataclass
from typing import Dict, Optional

import networkx as nx
from classes.domains import DomainDict


class LooperInterface:
    G: nx.Graph
    domains: DomainDict
    unplaced: list[str]
    tracker: Dict
    tracker_row: int
    curr_node: Optional[str]
    nb: Optional[str]

