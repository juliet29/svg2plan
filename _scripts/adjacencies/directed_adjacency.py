import networkx as nx
from typing import Dict
import math

from classes.domains import DomainDict
from classes.directions import Direction, pairs


class DirectedAdjacencyGenerator:
    def __init__(self, domains:DomainDict, graph: nx.Graph, node_a, node_b) -> None:
        self.domains = domains
        self.G = graph
        self.node_a = node_a
        self.node_b = node_b
        self.TOLERANCE = 0.01 # percent 
        self.run()

    def run(self):
        self.get_corners()
        self.make_horizontal_relation()
        self.make_vertical_relation()

    

    def update_nodes(self, direction):
        self.G.nodes[self.node_b]["data"][direction.name].append(self.node_a)

        self.G.nodes[self.node_a]["data"][pairs[direction].name].append(self.node_b)
        


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

  

    
    def get_corners(self):
        self.corners_a = self.domains[self.node_a].corners
        self.corners_b = self.domains[self.node_b].corners

    def is_equal(self):
       return math.isclose(self.corners_a[self.current_corner], self.corners_b[self.current_corner], rel_tol=self.TOLERANCE)

    
    def is_less_than(self, a, b):
        return self.corners_a[a] < self.corners_b[b]

    def is_greater_than(self, a, b):
        return self.corners_a[a] > self.corners_b[b]