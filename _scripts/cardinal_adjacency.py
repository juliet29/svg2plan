from enum import Enum

from classes.positioned_graph import PositionedGraph

class Direction(Enum):
    NORTH = 0
    SOUTH = 1
    EAST = 2
    WEST = 3



class CardinalAdjacency:
    def __init__(self, graph:PositionedGraph) -> None:
        self.layout = graph.layout
        self.G = graph.G
        self.curr_node = "m_bath"
        self.cardinal_adjacencies = {}



    def check_graph(self):
        for node in self.G:
            self.curr_node = node
            self.check_curr_node()

    def check_curr_node(self):
        self.dirs = [0, 1, 2, 3]
        for nb in list(self.G.neighbors(self.curr_node)):
            self.check_if_more_north(self.curr_node, nb)
            self.check_if_more_south(self.curr_node, nb)
            self.check_if_more_east(self.curr_node, nb)
            self.check_if_more_west(self.curr_node, nb)

        self.cardinal_adjacencies[self.curr_node] = [Direction(d) for d in self.dirs]



    def handle_direction(self, direction:int):
        if direction in self.dirs:
            self.dirs.remove(direction)



    def check_if_more_north(self, node:str, nb:str):
        if self.layout[nb][1] > self.layout[node][1]:
            self.handle_direction(Direction.NORTH.value)
        
    def check_if_more_south(self, node, nb):
        if self.layout[nb][1] < self.layout[node][1]:
            self.handle_direction(Direction.SOUTH.value)

    def check_if_more_east(self, node, nb):
        if self.layout[nb][0] > self.layout[node][0]:
            self.handle_direction(Direction.EAST.value)

    def check_if_more_west(self, node, nb):
        if self.layout[nb][0] < self.layout[node][0]:
            self.handle_direction(Direction.WEST.value)
        