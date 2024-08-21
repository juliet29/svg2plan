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
        self.G.nodes[self.b]["data"][direction.name].append(self.a)
        # print(f"{self.a} {direction.name} of {self.b}")

        self.G.nodes[self.a]["data"][pairs[direction].name].append(self.b)
        


    def make_horizontal_relation(self):
        self.current_corner = "x_left"
        if self.is_equal():
            print("equal x_left:", self.a, self.b)
            return

        # a EAST of b 
        if self.is_less_than2("x_right", "x_left"):
            self.update_nodes(Direction.EAST)
        elif self.is_greater_than2("x_left", "x_right"):
            self.update_nodes(Direction.WEST)



    def make_vertical_relation(self):
        self.current_corner = "y_top"

        if self.is_equal():
            print("equal y_top:", self.a, self.b)
            return
        
        # a SOUTH of b 
        if self.is_less_than2("y_top", "y_bottom"):
            self.update_nodes(Direction.SOUTH)
        elif self.is_greater_than2("y_bottom", "y_top"):
            self.update_nodes(Direction.NORTH)

  

    
    def get_corners(self):
        self.corners_a = self.domains[self.a].corners
        self.corners_b = self.domains[self.b].corners

    def is_equal(self):
       return math.isclose(self.corners_a[self.current_corner], self.corners_b[self.current_corner], rel_tol=self.TOLERANCE)

    
    def is_less_than2(self, a, b):
        return self.corners_a[a] < self.corners_b[b]

    def is_greater_than2(self, a, b):
        return self.corners_a[a] > self.corners_b[b]