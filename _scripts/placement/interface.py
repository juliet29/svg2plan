from dataclasses import dataclass
from typing import Dict, Optional

import networkx as nx
from svg_helpers.domains import DomainDict
from svg_helpers.layout import PartialLayout


class LooperInterface:
    G: nx.Graph
    init_domains: PartialLayout
    unplaced: list[str]
    tracker: Dict
    tracker_column: int
    curr_node: str
    new_domains: PartialLayout

