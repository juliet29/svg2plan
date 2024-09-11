import os
from typing import Dict, Callable
from dataclasses import dataclass
from enum import Enum
from copy import deepcopy
import json

import networkx as nx

from svg_helpers.directions import Direction
from svg_helpers.positioned_graph import PositionedGraph
from svg_helpers.helpers import get_bounds_of_layout

# todo for amber plan 01
LINKED_EDGES = [0, 3, 6, 10, 12, 16, 18, 19, 20, 21]

class SubsurfaceObjectType(Enum):
    DOOR = 0
    WINDOW = 1

@dataclass
class Subsurface:
    door_or_window: SubsurfaceObjectType
    id: int

    def to_json(self):
        return {
            "door_or_window": self.door_or_window.name,
            "id": self.id
        }
    

@dataclass
class Edge:
    edge: tuple
    is_linked: bool


class ConnectivityGenerator:
    def __init__(self, pos_graph: PositionedGraph) -> None:
        self.G_init = pos_graph.G
        self.layout = deepcopy(pos_graph.layout)
        self.G = deepcopy(pos_graph.G)

    def run(self):
        self.add_direction_nodes()
        self.add_windows()
        self.create_connectivity_template()
        self.update_connectivity_template()
        self.form_connectivity_graph()
        # self.write_to_file()

    def add_direction_nodes(self):
        for d in Direction:
            self.G.add_node(d.name, direction_node=True)
        self.update_layout_for_direction_nodes()

        self.G_rooms = nx.subgraph_view(self.G, filter_node=self.filter_direction_nodes)


    def add_windows(self):
        # TODO this may change for other floor plans..
        for key, data in self.G_rooms.nodes(data=True):
            empty_dir = data["data"].get_empty_directions()
            for d in empty_dir:
                if d == Direction.NORTH.name or d == Direction.SOUTH.name:
                    self.G.add_edge(key, Direction[d].name, data=Subsurface(SubsurfaceObjectType.WINDOW, 1))


    def create_connectivity_template(self):
        self.conn: Dict[int, Edge] = {}
        for ix, e in enumerate(self.G_rooms.edges):
            self.conn[ix] = Edge(e, False)

    def update_connectivity_template(self, linked_edges: list[int] = LINKED_EDGES):
        for ix in linked_edges:
            self.conn[ix].is_linked = True

    def form_connectivity_graph(self):
        for e in self.G_rooms.edges:
            if e not in [v.edge for v in self.conn.values() if v.is_linked == True]:
                self.G.remove_edge(*e)
            else:
                self.G.edges[e]["data"] = Subsurface(SubsurfaceObjectType.DOOR, 7)

        assert len(self.G.edges()) <= len(self.G_init.edges)

    def update_id(self, edges: list[tuple], id: int):
        for e in edges:
            try:
                self.G.edges[e]["data"].id = id
            except KeyError:
                print(f"invalid edge - {e}")
                pass
            

    def draw_graph(self):
        nx.draw(self.G, self.layout, with_labels=True)


    def write_to_file(self):
        self.jsonify_graph()
        path = os.path.join("../outputs", "amber_a", "graph.json")
        with open(path, "w+") as file:
            json.dump(self.G_json, default=str, fp=file)
        
    def jsonify_graph(self):
        self.G_json = nx.node_link_data(self.G)
        for d in self.G_json["links"]:
            d["data"] = d["data"].to_json()


######## direction stuff

    def filter_direction_nodes(self, node):
        try:
            self.G.nodes[node]["direction_node"]
            return False
        except:
            return True
        

    def update_layout_for_direction_nodes(self):
        c = get_bounds_of_layout(self.layout)
        print(c)
        mid_x = ((c.x_right - c.x_left)/2) + c.x_left
        mid_y = ((c.y_top - c.y_bottom)/2) + c.y_bottom
        print(mid_x, mid_y)

        PAD = 100

        self.layout[Direction.NORTH.name] = (mid_x, c.y_top+PAD)
        self.layout[Direction.SOUTH.name] = (mid_x, c.y_bottom-PAD)
        self.layout[Direction.EAST.name] = (c.x_left-PAD,mid_y)
        self.layout[Direction.WEST.name] = (c.x_right+PAD,mid_y)

    


    # def test_edge(self, e):
    #     return frozenset(e) in [frozenset(v.edge) for v in self.conn.values()]

    # def run_tests(self, test_fx: list[Callable[[Dict[int, Edge]], bool]]):
    #     for fx in test_fx:
    #         fx(self.conn)