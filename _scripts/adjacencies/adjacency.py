from typing import Dict
from itertools import combinations

from shapely import Polygon
import networkx as nx

from svg_helpers.graph_viz import draw_spring, draw_planar
from svg_helpers.shapely import list_coords
from svg_helpers.positioned_graph import PositionedGraph
from svg_helpers.domains import Domain
from svg_helpers.directions import NeighborDirections
from svg_helpers.layout import PartialLayout, Layout
from svg_helpers.constants import BUFFER_SIZE
from adjacencies.directed_adjacency import DirectedAdjacencyGenerator
 



class AdjacencyGenerator:
    def __init__(self, layout:PartialLayout, buffer_size=BUFFER_SIZE) -> None:
        self.partial_layout = layout
        self.buffer_size = buffer_size

    def run(self):
        self.initialize_graph()
        self.get_fp_layout()
        self.create_adjacencies()
        self.positioned_graph = PositionedGraph(self.G, self.fp_layout)
        self.create_layout()

    def initialize_graph(self):
        self.G = nx.Graph()
        nodes = [(domain, 
                  {"data": NeighborDirections()}) 
                  for domain in self.partial_layout.domains]
        self.G.add_nodes_from(nodes)

    def create_adjacencies(self):
        self.pairs = list(combinations(self.partial_layout.shapes.keys(), 2))
        for a, b in self.pairs:
            if self.check_adjacency(self.partial_layout.shapes[a], self.partial_layout.shapes[b]):
                self.G.add_edge(a, b)
                self.DAG = DirectedAdjacencyGenerator(self.partial_layout, self.G, a, b)


    def check_adjacency(self, a:Polygon, b:Polygon):
        sz = self.buffer_size
        return a.buffer(sz).intersects(b.buffer(sz))
    
    def create_layout(self):
        self.layout = Layout(self.layout.shapes, self.layout.domains, self.G)


    ## display... 

    def get_fp_layout(self):
        self.fp_layout = {}
        for k, v in self.partial_layout.shapes.items():
            top_right_corner = list_coords(v.exterior.coords)[2]
            self.fp_layout[k] = top_right_corner
    

    def draw_graph(self, NEW=False):
        if self.G:
            if NEW:
                try:
                    self.auto_layout = draw_planar(self.G)
                except:
                    self.auto_layout = draw_spring(self.G)
            else:
                nx.draw(self.G, self.fp_layout, with_labels=True)
            
            