from typing import Optional
from placement.interface import LooperInterface, NodeNotFoundExcepton
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
            raise NodeNotFoundExcepton("too many nw nodes!")
        return True

    def find_west_node(self):
        nbs = self.lo.G.nodes[self.lo.curr_node]["data"][Direction.WEST.name]
        # node must already have been placed in self.lo.new_domains

        if not nbs:
            print(f"no west node for {self.lo.curr_node}")
            raise NodeNotFoundExcepton

        if len(nbs) == 1:
            return nbs[0]
        else:
            return self.find_best_node(Direction.EAST, nbs, self.lo.curr_node)

    def find_next_directed_node(self, direction: Direction, ref_node: str):
        nbs = self.lo.G.nodes[ref_node]["data"][direction.name]
        nbs = list(set(nbs).intersection(set(self.lo.unplaced)))

        if not nbs:
            raise NodeNotFoundExcepton
        try:
            [self.lo.curr_node] = nbs
        except ValueError:
                self.lo.curr_node = self.find_best_node(direction, nbs, ref_node)


    def find_best_node(self, direction: Direction, candidates: list, ref_node):
        corner = match_corner(direction)
        difs = [abs(self.get_val(node, corner) - self.get_val(ref_node, corner)) for node in candidates]
        index_of_closest_corner = difs.index(min(difs))

        print(f"finding node closest to {ref_node} in {direction.name} direction... looking for closest {corner}")
        print(list(zip(candidates,difs)))

        return candidates[index_of_closest_corner]
    
    def get_val(self, node, corner):
        return self.lo.init_layout.corners[node][corner]
    

def match_corner(direction: Direction):
    match direction:
        case Direction.EAST:
            return "y_top"
        case Direction.SOUTH:
            # print("finding best node. before this was x_right. now it is x_left. if room stacking fails, this may be why :)")
            return "x_left"
        case _:
            raise Exception("Invalid direction for matching a corner")
