import os
from typing import Dict, Callable
from dataclasses import dataclass
from enum import Enum
from copy import deepcopy
import json

import networkx as nx

from svg_helpers.directions import Direction
from svg_helpers.positioned_graph import PositionedGraph

LINKED_EDGES = [0, 3, 6, 10, 12, 16, 18, 19, 20, 21]


class WindowType(Enum):
    A = 0
    B = 1


@dataclass
class Window:
    direction: Direction
    window_type: WindowType

    def to_json(self):
        return {
            "direction": self.direction.name,
            "window_type": self.window_type.name
        }


@dataclass
class Edge:
    edge: tuple
    is_linked: bool


class ConnectivityGenerator:
    def __init__(self, pos_graph: PositionedGraph) -> None:
        self.G_init = pos_graph.G
        self.layout = pos_graph.layout
        self.G = deepcopy(pos_graph.G)

    def run(self):
        self.add_windows()
        self.create_connectivity_template()
        self.update_connectivity_template()
        self.form_connectivity_graph()
        self.write_to_file()

    def add_windows(self):
        # TODO this may change for other floor plans..
        for key, data in self.G.nodes(data=True):
            data["windows"] = []
            empty_dir = data["data"].get_empty_directions()
            for d in empty_dir:
                if d == Direction.NORTH.name or d == Direction.SOUTH.name:
                    data["windows"].append(Window(Direction[d], WindowType.A))

    def create_connectivity_template(self):
        self.conn: Dict[int, Edge] = {}
        for ix, e in enumerate(self.G.edges):
            self.conn[ix] = Edge(e, False)

    def update_connectivity_template(self, linked_edges: list[int] = LINKED_EDGES):
        for ix in linked_edges:
            self.conn[ix].is_linked = True

    def test_edge(self, e):
        return frozenset(e) in [frozenset(v.edge) for v in self.conn.values()]

    # def run_tests(self, test_fx: list[Callable[[Dict[int, Edge]], bool]]):
    #     for fx in test_fx:
    #         fx(self.conn)

    def form_connectivity_graph(self):
        for e in self.G.edges:
            if e not in [v.edge for v in self.conn.values() if v.is_linked == True]:
                self.G.remove_edge(*e)

        assert len(self.G.edges()) <= len(self.G_init.edges)

    def draw_graph(self):
        nx.draw(self.G, self.layout, with_labels=True)


    def write_to_file(self):
        self.jsonify_graph()
        path = os.path.join("../outputs", "amber_a", "graph.json")
        with open(path, "w+") as file:
            json.dump(self.G_json, default=str, fp=file)
        
    def jsonify_graph(self):
        self.G_json = nx.node_link_data(self.G)
        for item in self.G_json["nodes"]:
            item["data"] = item["data"].to_json()
            item["windows"] = [i.to_json() for i in item["windows"]]

    
