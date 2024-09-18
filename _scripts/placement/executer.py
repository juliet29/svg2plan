from networkx import Graph
from copy import deepcopy
import logging

from svg_helpers.domains import DomainDict
from svg_helpers.directions import Direction
from placement.finder import Finder
from placement.updater import Updater
from placement.placer import Placer
from placement.interface import LooperInterface, NodeNotFoundExcepton
from svg_helpers.shapely import create_box_from_decimal_corners
from svg_helpers.layout import PartialLayout, Layout
from svg_helpers.domains import DecimalCorners, empty_decimal_corner
from decimal import Decimal

logger = logging.getLogger(__name__)



class PlacementExecuter(LooperInterface):
    def __init__(self, layout: Layout) -> None:
        self.G = deepcopy(layout.graph)
        self.init_layout = PartialLayout(deepcopy(layout.shapes), deepcopy(layout.corners))

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
        self.prepare_data_for_export()

    def init_new_domains(self):
        empty_corner = {k: empty_decimal_corner for k in self.init_layout.corners.keys()}
        self.new_domains = PartialLayout({}, empty_corner)

    def set_north_west_node(self):
        self.finder.find_north_west_node()
        self.placer.place_north_west_node()
        self.updater.update_tracker()
        self.updater.update_unplaced()

    def set_remaining_north_nodes(self):
        self.ew_counter = 0
        while True:
            west_node = self.tracker[self.tracker_column][0]
            try:
                self.finder.find_next_directed_node(Direction.EAST, west_node)
            except NodeNotFoundExcepton: 
                logger.debug(f"{self.curr_node} has no western nbs that are unplaced")
                return
            
            self.placer.place_next_east_node(west_node)
            self.tracker_column += 1
            self.updater.update_tracker()
            self.updater.update_unplaced()

            if self.is_over_ew_counter():
                logger.warning("ew_counter > 5 .. breaking")
                return

    def set_relative_south_nodes(self):
        self.ns_counter = 0
        self.north_node_reference = 0

        while len(self.unplaced) > 0:
            for column in self.tracker.values():
                try:
                    north_node = column[self.north_node_reference]
                    logger.debug(f"current north node: {north_node}")
                except IndexError:
                    logger.debug(f"{column} < {self.north_node_reference}")
                    continue

                try:
                    self.finder.find_next_directed_node(
                        Direction.SOUTH, north_node
                    )
                except NodeNotFoundExcepton:
                    logger.debug(f"no more southern nbs for {north_node}")
                    continue
                
                self.finish_setting_south_node(north_node, column)
                
                if len(self.unplaced) == 0:
                    logger.debug("no more nodes to place")
                    return

            self.north_node_reference += 1
            logger.debug(
                f"changing north node reference to {self.north_node_reference}. Number of unplaced nodes is {len(self.unplaced)}"
            )

            if self.is_over_ns_counter():
                logger.warning("ns_counter > 4 .. breaking")
                break

    def finish_setting_south_node(self, north_node, column):
        try: 
            west_node = self.finder.find_west_node()
            self.placer.place_next_south_node(north_node, west_node)
        except:
            self.placer.place_next_south_node(north_node)

        self.updater.extend_tracker_south(column)
        self.updater.update_unplaced()


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
        for name, corner in self.new_domains.corners.items():
            self.shapes[name] = create_box_from_decimal_corners(corner)
        self.layout = Layout(self.shapes, self.new_domains.corners, self.G)

