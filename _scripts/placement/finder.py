from typing import Optional
from placement.interface import LooperInterface
from svg_helpers.directions import Direction


class Finder:
    def __init__(self, looper_obj: LooperInterface) -> None:
        self.lo = looper_obj

    def find_north_west_node(self):
        ne_nodes = []
        for k, v in self.lo.G.nodes(data=True):
            if not v["data"].NORTH and not v["data"].WEST:
                ne_nodes.append(k)

        [self.lo.curr_node] = ne_nodes
        return True

    def find_west_node(self):
        nbs = self.lo.G.nodes[self.lo.curr_node]["data"][Direction.WEST.name]
        # node must already have been placed in self.lo.new_domains

        if not nbs:
            return None

        if len(nbs) == 1:
            return nbs[0]
        else:
            return self.find_best_node("x_right", nbs)

    def find_next_directed_node(self, direction: Direction, ref_node: str):
        nbs = self.lo.G.nodes[ref_node]["data"][direction.name]
        nbs = list(set(nbs).intersection(set(self.lo.unplaced)))

        if not nbs:
            return False
        try:
            [self.lo.curr_node] = nbs
        except ValueError:
            corner = match_corner(direction)
            self.lo.curr_node = self.find_best_node(corner, nbs)
        return True

    def find_best_node(self, corner, candidates):
        corners = [self.lo.init_layout.corners[node][corner] for node in candidates]
        index_of_greatest_corner = corners.index(max(corners))
        return candidates[index_of_greatest_corner]


def match_corner(direction: Direction):
    match direction:
        case Direction.EAST:
            return "y_top"
        case Direction.SOUTH:
            return "x_right"
        case _:
            raise Exception("Invalid direction for matching a corner")
