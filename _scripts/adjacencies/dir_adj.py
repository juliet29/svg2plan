import networkx as nx
from typing import Dict
import math

from svg_helpers.domains import DomainDict
from svg_helpers.directions import Direction, DIRECTION_PAIRS
from svg_helpers.layout import PartialLayout
from graphtype import Graph, GraphData, NodeData, EdgeData, validate

class DirectedAdjacencyGenerator:
    # TODO rfactor this. 
    def __init__(self, layout: PartialLayout, graph: nx.Graph, node_a, node_b) -> None:
        self.layout = layout
        self.G = graph
        self.node_a = node_a
        self.node_b = node_b
        self.TOLERANCE = 0.01  # percent

    def get_domains(self):
        self.domains_a = self.layout.domains[self.node_a]
        self.domains_b = self.layout.domains[self.node_b]
        self.cmp = self.domains_a.compare_domains(self.domains_b)

        for drn, domain in self.cmp:
            if domain: 
                self.G.nodes[domain.name][drn].append(domain.name)


