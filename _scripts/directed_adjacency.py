import networkx as nx
from typing import Dict
import math

from classes.domains import Domain
from classes.directions import Direction, pairs



class DirectedAdjacencyGenerator:
    def __init__(self, domains:Dict[str, Domain], graph: nx.Graph, a, b) -> None:
        self.domains = domains
        self.G = graph
        self.a = a
        self.b = b
        self.TOLERANCE = 0.01 # percent 
        self.run()

    def run(self):
        self.get_corners()
        self.make_horizontal_relation()
        self.make_vertical_relation()

    

    def update_nodes(self, direction):
        self.G.nodes[self.b]["neighbor_directions"][direction.name].append(self.a)
        print(f"{self.a} {direction.name} of {self.b}")

        self.G.nodes[self.a]["neighbor_directions"][pairs[direction].name].append(self.b)
        


    def make_horizontal_relation(self):
        if self.is_equal("x_left"):
            return

        # a EAST of b 
        if self.is_less_than("x_left"):
            self.update_nodes(Direction.EAST)

        # a WEST of b 
        elif self.is_greater_than("x_left"):
            
            self.update_nodes(Direction.WEST)


    def make_vertical_relation(self):
        if self.is_equal("y_top"):
            return
        # a SOUTH of b 
        if self.is_less_than("y_top"):
            self.update_nodes(Direction.SOUTH)
        # a NORTH of b   
        elif self.is_greater_than("y_top"):
            self.update_nodes(Direction.NORTH)

    
    def get_corners(self):
        self.corners_a = self.domains[self.a].corners
        self.corners_b = self.domains[self.b].corners

    def is_equal(self, corner):
       return math.isclose(self.corners_a[corner], self.corners_b[corner], rel_tol=self.TOLERANCE)
    
    def is_less_than(self, corner):
        return self.corners_a[corner] < self.corners_b[corner]

    def is_greater_than(self, corner):
        return self.corners_a[corner] > self.corners_b[corner]