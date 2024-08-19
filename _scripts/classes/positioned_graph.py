from dataclasses import dataclass
from typing import Dict
import networkx as nx

@dataclass
class PositionedGraph:
    G: nx.Graph
    layout: Dict[str, tuple]
