from dataclasses import dataclass
from typing import Dict, Optional

import networkx as nx
from svg_helpers.domains import DomainDict


class LooperInterface:
    G: nx.Graph
    domains: DomainDict
    unplaced: list[str]
    tracker: Dict
    tracker_column: int
    curr_node: str

