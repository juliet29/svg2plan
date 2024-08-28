from typing import Optional
from classes.directions import Direction

class Finder:
    def __init__(self, looper_obj) -> None:
        self.lo = looper_obj


    def find_next_south_node(self):
        if self.lo.curr_node is None:
            self.find_north_east_node()

        else:
            self.search_for_southern_nodes()

        return True



    def find_north_east_node(self):
        ne_nodes = []
        for k, v in self.lo.G.nodes(data=True):
            if not v["data"].NORTH and not v["data"].EAST:
                ne_nodes.append(k)

        # there should only be on ne node
        [self.lo.curr_node] = ne_nodes
        # print(f"ne node is {self.lo.curr_node}")
        return True
    
    def search_for_southern_nodes(self):
        for curr_node in self.lo.tracker[self.lo.tracker_row - 1]:
            # print(f"curr_node in row {self.lo.tracker_row - 1} = {curr_node}")

            if self.find_next_directed_node(Direction.SOUTH, curr_node):
                # print(f"next south node is {self.lo.nb}")
                self.lo.curr_node = self.lo.nb
                return True
            else:
                # print(f"---{curr_node} has no southern nbs that are unplaced")
                continue

                # updating to mirror behavior of find_north_east_node
                


    def find_next_directed_node(self, direction:Direction, curr_node:Optional[str]=None):
        if not curr_node:
            curr_node = self.lo.curr_node
        nbs = self.lo.G.nodes[curr_node]["data"][direction.name]
        available_nbs = list(set(nbs).intersection(set(self.lo.unplaced)))
        if not available_nbs:
            return False

        try:
            [self.lo.nb] = available_nbs
            return True
        except ValueError:
            # more than one nb
            corner = "y_top" if direction.name == "WEST" else "x_right"
            corners = [self.lo.domains[node].corners[corner] for node in available_nbs]
            index_of_greatest_corner = corners.index(max(corners))
            self.lo.nb = available_nbs[index_of_greatest_corner]
            return True
