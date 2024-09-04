from networkx import Graph
from copy import deepcopy

from svg_helpers.domains import DomainDict
from svg_helpers.directions import Direction
from placement.finder import Finder
from placement.updater import Updater
from placement.placer import Placer
from placement.interface import LooperInterface
from svg_helpers.shapely import create_box_from_corners


class PlacementExecuter(LooperInterface):
    def __init__(self, graph: Graph, domains: DomainDict) -> None:
        self.G = deepcopy(graph)
        self.domains = deepcopy(domains)

        self.unplaced = list(self.G.nodes)
        self.tracker = {}
        self.tracker_column = 0
        self.curr_node = ""

        self.finder = Finder(self)
        self.updater = Updater(self)
        self.placer = Placer(self)

    def run(self):
        self.set_north_west_node()
        self.set_remaining_north_nodes()
        self.set_relative_south_nodes()
        self.clean_up()

    def set_north_west_node(self):
        self.finder.find_north_west_node()
        self.placer.place_north_west_node()
        self.updater.update_tracker()
        self.updater.update_unplaced()

    def set_remaining_north_nodes(self):
        self.ew_counter = 0
        while True:
            west_node = self.tracker[self.tracker_column][0]
            if not self.finder.find_next_directed_node(Direction.EAST, west_node):
                print(f"---{self.curr_node} has no western nbs that are unplaced")
                return
            else:
                self.placer.place_next_east_node(west_node)
                self.tracker_column += 1
                self.updater.update_tracker()
                self.updater.update_unplaced()

            if self.is_over_ew_counter():
                print("ew_counter > 5 .. breaking")
                return

    def set_relative_south_nodes(self):
        self.ns_counter = 0
        north_node_reference = 0

        while len(self.unplaced) > 0:
            for key, column in self.tracker.items():
                try:
                    north_node = column[north_node_reference]
                except:
                    print(
                        f"north node = {north_node}. getting index {north_node_reference} in {column} failed"
                    )
                    break
                # sets the nb
                result = self.finder.find_next_directed_node(
                    Direction.SOUTH, north_node
                )
                if result == True:
                    west_node = self.finder.find_west_node()
                    self.placer.place_next_south_node(north_node, west_node)
                    self.updater.extend_tracker_south(column)
                    self.updater.update_unplaced()

                if len(self.unplaced) == 0:
                    print("no more nodes to place")
                    return

            north_node_reference += 1
            print(
                f"changing north node reference to {north_node_reference}. Number of unplaced nodes is {len(self.unplaced)}"
            )

            if self.is_over_ns_counter():
                print("ns_counter > 4 .. breaking")
                break

    def is_over_ns_counter(self):
        self.ns_counter += 1
        if self.ns_counter > 4:
            return True

    def is_over_ew_counter(self):
        self.ew_counter += 1
        if self.ew_counter > 5:
            return True

    def clean_up(self):
        self.shapes = {}
        self.corners = {}
        for name, room in self.domains.items():
            self.corners[name] = room.new_corners
            self.shapes[name] = create_box_from_corners(room.new_corners)
