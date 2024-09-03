from classes.layout import Layout
from classes.directions import Direction
from problems.classes.problems_base import ProblemsBase

SIDE_HOLE_PAIRS = {
    Direction.NORTH : [Direction.EAST, Direction.WEST],
    Direction.SOUTH : [Direction.EAST, Direction.WEST],
    Direction.EAST : [Direction.NORTH, Direction.SOUTH],
    Direction.WEST : [Direction.NORTH, Direction.SOUTH],
}


class SideHoleFinder(ProblemsBase):
    def __init__(self, layout:Layout) -> None:
        super().__init__(layout)
        self.side_hole_pairs = []

    def search_layout(self):
        for dir in Direction:
            self.direction = dir
            for node, data in self.G.nodes(data=True):
                if not data["data"][dir.name]:
                    self.node = node
                    self.node_data = data["data"]
                    self.search_near_node()
             

    def search_near_node(self):
        nbs = self.find_direction_nbs()
        
        for nb in nbs:
            if not self.shapes[self.node].touches(self.shapes[nb]):
                    self.side_hole_pairs.append((self.node, nb))

    def find_direction_nbs(self):
        dir1, dir2 = SIDE_HOLE_PAIRS[self.direction]
        nbs = self.node_data[dir1.name] + self.node_data[dir2.name]
        true_nbs = [n for n in nbs 
                    if not self.G.nodes[n]["data"][self.direction.name]]
        return true_nbs

