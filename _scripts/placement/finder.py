from typing import Optional
from placement.interface import LooperInterface
from svg_helpers.directions import Direction


class Finder:
    def __init__(self, looper_obj: LooperInterface) -> None:
        self.lo = looper_obj 

    def find_north_west_node(self):
        nw_nodes = []
        for k, v in self.lo.G.nodes(data=True):
            if not v["data"].NORTH and not v["data"].WEST:
                nw_nodes.append(k)

        try:
            [self.lo.curr_node] = nw_nodes
        except:
            print(f"ne_nodes: {nw_nodes}")
            raise Exception("too many nw nodes!")
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
            if direction == Direction.SOUTH:
                print("matching a south corner! NOTE this was changed for amber b!")
                self.lo.curr_node = self.find_best_node_south(corner, nbs)
            else:
                self.lo.curr_node = self.find_best_node(corner, nbs)
        return True

    def find_best_node(self, corner, candidates):
        corners = [self.lo.init_layout.corners[node][corner] for node in candidates]
        index_of_greatest_corner = corners.index(max(corners))
        return candidates[index_of_greatest_corner]
    

    def find_best_node_south(self, corner, candidates):
        corners = [self.lo.init_layout.corners[node][corner] for node in candidates]
        index_of_greatest_corner = corners.index(min(corners))
        return candidates[index_of_greatest_corner]

def match_corner(direction: Direction):
    match direction:
        case Direction.EAST:
            return "y_top"
        case Direction.SOUTH:
            # print("finding best node. before this was x_right. now it is x_left. if room stacking fails, this may be why :)")
            return "x_right"
        case _:
            raise Exception("Invalid direction for matching a corner")
