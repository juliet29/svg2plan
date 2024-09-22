import logging
from typing import Dict

import networkx as nx
from svg_helpers.domains import DomainDict
from svg_helpers.layout import PartialLayout


stack_logger = logging.getLogger(__name__)


class LooperInterface:
    G: nx.Graph
    init_layout: PartialLayout
    unplaced: list[str]
    tracker: Dict
    tracker_column: int
    curr_node: str
    new_layout: PartialLayout


class NodeNotFoundExcepton(Exception):
    pass
