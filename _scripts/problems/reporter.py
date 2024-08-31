from typing import Dict
from dataclasses import dataclass
import networkx as nx
from shapely import Polygon, intersection, union_all, STRtree, LinearRing
from pprint import pprint

from svg_helpers.helpers import key_from_value


@dataclass
class Overlap:
    rooms: tuple[str]
    geometry: Polygon

@dataclass
class Hole:
    rooms: tuple[str]
    hole_geometry: Polygon



class Reporter:
    def __init__(self, shapes:Dict[str, Polygon], G: nx.Graph) -> None:
        self.shapes = shapes
        self.G = G

    def run(self):
        self.find_overlaps()
        self.find_holes()
        self.summarize()

    def find_overlaps(self):
        self.overlaps = []
        for e in self.G.edges:
            u, v = e
            if self.shapes[u].overlaps(self.shapes[v]):
                geometry = intersection(self.shapes[u], self.shapes[v])
                assert isinstance(geometry, Polygon) 
                self.overlaps.append(
                    Overlap(e, geometry))

    def find_holes(self):
        self.holes = []
        self.union = union_all(list(self.shapes.values()))
        assert isinstance(self.union, Polygon) 

        self.tree = STRtree(list(self.shapes.values()))
        for hole in self.union.interiors:
            assert isinstance(hole, LinearRing) 
            self.holes.append(
                Hole(self.find_rooms_surrounding_hole(), Polygon(hole)))
            

            
    def find_rooms_surrounding_hole(self):
        assert isinstance(self.union, Polygon) 
        indices = self.tree.query_nearest(self.union.interiors[0])
        nearest = self.tree.geometries.take(indices).tolist()
        rooms = tuple([key_from_value(self.shapes, p) for p in nearest])
        return rooms
        


    def summarize(self):
        print(f"Overlaps: {len(self.overlaps)}. Holes: {len(self.holes)}.")
        print([o.rooms for o in self.overlaps])
        print([o.rooms for o in self.holes])

        