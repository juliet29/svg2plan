from typing import Dict
from itertools import combinations

from shapely import Polygon
import networkx as nx

from helpers.graph_viz import draw_spring, draw_planar
from helpers.shapely import list_coords
from classes.positioned_graph import PositionedGraph
from classes.domains import Domain
from classes.directions import NeighborDirections
from directed_adjacency import DirectedAdjacencyGenerator



class AdjacencyGenerator:
    def __init__(self, domains:Dict[str, Domain]) -> None:
        self.domains = domains

    def run(self):
        self.initialize_graph()
        self.get_layout()
        self.update_adjacencies()
        self.positioned_graph = PositionedGraph(self.G, self.fp_layout)

    def initialize_graph(self):
        self.G = nx.Graph()
        nodes = [(domain, 
                  {"data": NeighborDirections()}) 
                  for domain in self.domains]
        self.G.add_nodes_from(nodes)

    def update_adjacencies(self):
        self.pairs = list(combinations(self.domains.keys(), 2))
        for a, b in self.pairs:
            if self.check_adjacency(self.domains[a].polygon, self.domains[b].polygon):
                self.G.add_edge(a, b)
                self.DAG = DirectedAdjacencyGenerator(self.domains, self.G, a, b)


    def check_adjacency(self, a:Polygon, b:Polygon, buffer_size=30):
        return a.buffer(buffer_size).intersects(b.buffer(buffer_size))
    

    # TODO could be its own class, needs the strings, the graph, and the domains.. 


    ## graph stuff

    def get_layout(self):
        self.fp_layout = {}
        for k, v in self.domains.items():
            top_right_corner = list_coords(v.polygon.exterior.coords)[2]
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
            
            