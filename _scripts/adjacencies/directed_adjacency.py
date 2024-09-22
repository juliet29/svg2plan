import networkx as nx
from typing import Dict
import math

from svg_helpers.domains import DomainDict
from svg_helpers.directions import Direction, DIRECTION_PAIRS
from svg_helpers.layout import PartialLayout


class DirectedAdjacencyGenerator:
    # TODO rfactor this. 
    def __init__(self, layout: PartialLayout, graph: nx.Graph, node_a, node_b) -> None:
        self.layout = layout
        self.G = graph
        self.node_a = node_a
        self.node_b = node_b
        self.TOLERANCE = 0.01  # percent
        self.run()

    def run(self):
        self.get_domains()
        self.make_horizontal_relation()
        self.make_vertical_relation()

    def update_nodes(self, direction):
        self.G.nodes[self.node_b]["nb_dirs"][direction.name].append(self.node_a)

        self.G.nodes[self.node_a]["nb_dirs"][DIRECTION_PAIRS[direction].name].append(
            self.node_b
        )

    def make_horizontal_relation(self):
        self.current_corner = "x_left"
        if self.is_equal():
            return

        # a EAST of b
        if self.is_less_than("x_right", "x_left"):
            self.update_nodes(Direction.WEST)
        elif self.is_greater_than("x_left", "x_right"):
            self.update_nodes(Direction.EAST)

    def make_vertical_relation(self):
        self.current_corner = "y_top"

        if self.is_equal():
            return

        # a SOUTH of b
        if self.is_less_than("y_top", "y_bottom"):
            self.update_nodes(Direction.SOUTH)
        elif self.is_greater_than("y_bottom", "y_top"):
            self.update_nodes(Direction.NORTH)

    def get_domains(self):
        self.domains_a = self.layout.domains[self.node_a]
        self.domains_b = self.layout.domains[self.node_b]

    def is_equal(self):
        return math.isclose(
            self.domains_a[self.current_corner],
            self.domains_b[self.current_corner],
            rel_tol=self.TOLERANCE,
        )

    def is_less_than(self, a, b):
        return self.domains_a[a] < self.domains_b[b]

    def is_greater_than(self, a, b):
        return self.domains_a[a] > self.domains_b[b]
