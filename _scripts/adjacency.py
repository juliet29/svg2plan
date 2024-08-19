from typing import Dict
from itertools import combinations

from shapely import LinearRing, Polygon
import networkx as nx

from helpers.graph_viz import draw_spring, draw_planar
from helpers.shapely import get_point_as_xy
from positioned_graph import PositionedGraph



class AdjacencyGenerator:
    def __init__(self, domains:Dict[str, Polygon]) -> None:
        self.domains = domains

    def run(self):
        self.initialize_graph()
        self.get_fp_layout()
        self.update_adjacencies()
        self.pos_graph = PositionedGraph(self.G, self.fp_layout)

    def initialize_graph(self):
        self.G = nx.Graph()
        self.G.add_nodes_from(self.domains.keys())

    def update_adjacencies(self):
        pairs = list(combinations(self.domains.keys(), 2))
        for a, b in pairs:
            if self.check_adjacency(self.domains[a], self.domains[b]):
                self.G.add_edge(a, b)


    def check_adjacency(self, a:Polygon, b:Polygon, buffer_size=30):
        return a.buffer(buffer_size).intersects(b.buffer(buffer_size))
    
    def get_fp_layout(self):
        self.fp_layout = {}
        for k, v in self.domains.items():
            self.fp_layout[k]  = get_point_as_xy(v.centroid)

    
    
    def draw_graph(self, NEW=False):
        if self.G:
            if NEW:
                try:
                    self.auto_layout = draw_planar(self.G)
                except:
                    self.auto_layout = draw_spring(self.G)
            else:
                nx.draw(self.G, self.fp_layout, with_labels=True)
            
            