from networkx import Graph
from copy import deepcopy

from svg_helpers.domains import DomainDict
from svg_helpers.directions import Direction
from placement.finder import Finder
from placement.updater import Updater
from placement.placer import Placer
from placement.interface import LooperInterface
from svg_helpers.shapely import create_box_from_corners, create_box_from_decimal_corners
from svg_helpers.layout import PartialLayout
from svg_helpers.domains import DecimalCorners, empty_decimal_corner
from decimal import Decimal


class PlacementExecuter(LooperInterface):
    def __init__(self, graph: Graph, domains: PartialLayout) -> None:
        self.G = deepcopy(graph)
        self.init_domains= deepcopy(domains)


        self.unplaced = list(self.G.nodes)
        self.tracker = {}
        self.tracker_column = 0
        self.curr_node = ""

        self.finder = Finder(self)
        self.updater = Updater(self)
        self.placer = Placer(self)

    def run(self):
        self.init_new_domains()
        self.set_north_west_node()
        self.set_remaining_north_nodes()
        self.set_relative_south_nodes()
        # self.prepare_data_for_export()

    def init_new_domains(self):
        empy_corner = {k: empty_decimal_corner for k in self.init_domains.corners.keys()}
        self.new_domains = PartialLayout({}, empy_corner)

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
        self.north_node_reference = 0

        while len(self.unplaced) > 0:
            for key, column in self.tracker.items():
                try:
                    north_node = column[self.north_node_reference]
                except:
                    print(
                        f"north node = {north_node}. getting index {self.north_node_reference} in {column} failed"
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

            self.north_node_reference += 1
            print(
                f"changing north node reference to {self.north_node_reference}. Number of unplaced nodes is {len(self.unplaced)}"
            )

            if self.is_over_ns_counter():
                print("ns_counter > 4 .. breaking")
                break

    # def look_for_north_node(self):



    # TODO make ns and ew counter a class argument 
    def is_over_ns_counter(self):
        self.ns_counter += 1
        if self.ns_counter > 4:
            return True

    def is_over_ew_counter(self):
        self.ew_counter += 1
        if self.ew_counter > 5:
            return True

    def prepare_data_for_export(self):
        self.shapes = {}
        self.corners = {}
        for name, corner in self.init_domains.corners.items():
            self.corners[name] = corner
            self.shapes[name] = create_box_from_decimal_corners(corner)
        # TODO make into a layout object 
