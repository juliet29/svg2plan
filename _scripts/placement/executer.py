from typing import Dict
from networkx import Graph
from copy import deepcopy
import logging

from helpers.directions import Direction
from placement.finder import Finder
from placement.updater import Updater
from placement.placer import Placer
from placement.interface import LooperInterface, NodeNotFoundExcepton, stack_logger
from helpers.shapely import domain_to_shape
from helpers.layout import PartialLayout, Layout


class PlacementExecuter(LooperInterface):
    def __init__(self, layout: Layout, ns_counter_max=10) -> None:
        stack_logger.info("\n begining to execute stacking")
        self.G = deepcopy(layout.graph)
        self.init_layout = PartialLayout(
            deepcopy(layout.shapes), deepcopy(layout.domains)
        )
        self.ns_counter_max = ns_counter_max
        self.unplaced = list(self.G.nodes)
        self.tracker: Dict[int, list[str]] = {}
        self.tracker_column = 0
        self.curr_node = ""

        self.finder = Finder(self)
        self.updater = Updater(self)
        self.placer = Placer(self)

    def run(self):
        self.init_new_layout()
        self.set_north_west_node()
        self.set_remaining_north_nodes()
        self.set_relative_south_nodes()
        self.prepare_data_for_export()

    def init_new_layout(self):
        empty_domains = {k: None for k in self.init_layout.domains.keys()}
        self.new_layout = PartialLayout({}, empty_domains)  # type: ignore

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
                stack_logger.debug(
                    f"{self.curr_node} has no eastern nbs that are unplaced"
                )
                return

            self.placer.place_next_east_node(west_node)
            self.tracker_column += 1
            self.updater.update_tracker()
            self.updater.update_unplaced()

            if self.is_over_ew_counter():
                stack_logger.warning("ew_counter > 5 .. breaking")
                return

    def set_relative_south_nodes(self):
        self.ns_counter = 0
        self.north_node_reference = 0  # row

        while len(self.unplaced) > 0:
            for (
                col_num,
                column,
            ) in (
                self.tracker.items()
            ):  # northern most node marks beginning of a column => TODO maybe a custom data structure..
                try:
                    north_node = column[self.north_node_reference]
                    stack_logger.debug(f"current north node: {north_node}")
                except IndexError:
                    stack_logger.debug(f"{column} < {self.north_node_reference}")
                    continue

                try:
                    self.finder.find_next_directed_node(Direction.SOUTH, north_node)
                except NodeNotFoundExcepton:
                    stack_logger.debug(f"no more southern nbs for {north_node}")
                    continue

                self.finish_setting_south_node(north_node, column, col_num)

                if len(self.unplaced) == 0:
                    stack_logger.debug("no more nodes to place")
                    return

            self.north_node_reference += 1
            stack_logger.debug(
                f"changing north node reference to {self.north_node_reference}. Number of unplaced nodes is {len(self.unplaced)}"
            )

            if self.is_over_ns_counter():
                stack_logger.warning(f"ns_counter > {self.ns_counter_max} .. breaking")
                break

    def finish_setting_south_node(
        self, north_node: str, column: list[str], col_num: int
    ):
        try:
            west_node = self.finder.find_west_node()
            self.placer.place_next_south_node(north_node, col_num, west_node)
        except:
            self.placer.place_next_south_node(north_node, col_num, None)

        self.updater.extend_tracker_south(column)
        self.updater.update_unplaced()

    # TODO make ns and ew counter a class argument
    def is_over_ns_counter(self):
        self.ns_counter += 1
        if self.ns_counter > self.ns_counter_max:
            return True

    def is_over_ew_counter(self):
        self.ew_counter += 1
        if self.ew_counter > 5:
            return True

    def prepare_data_for_export(self):
        self.shapes = {}
        for name, domain in self.new_layout.domains.items():
            self.shapes[name] = domain_to_shape(domain)
        self.layout = Layout(self.shapes, self.new_layout.domains, self.G)
