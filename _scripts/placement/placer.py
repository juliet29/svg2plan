import logging
from placement.interface import LooperInterface, stack_logger
from svg_helpers.constants import ROUNDING_LIM
from svg_helpers.domains import Corners, DecimalCorners, empty_decimal_corner
from svg_helpers.decimal_operations import decimal_mult, decimal_add, decimal_sub
from decimal import Decimal
from new_corners.domain import Domain
from log_setter.log_settings import svlogger


class Placer:
    def __init__(self, looper_obj: LooperInterface) -> None:
        self.lo = looper_obj

    def place_north_west_node(self):
        new_x_left = Decimal(0)
        new_y_top = Decimal(0)
        self.create_new_corners(self.lo.curr_node, new_x_left, new_y_top)

    def place_next_east_node(self, west_node):
        new_y_top = Decimal(0)
        new_x_left = self.lo.new_layout.domains[west_node].x.max
        self.create_new_corners(self.lo.curr_node, new_x_left, new_y_top)

    def place_next_south_node(
        self, north_node: str, col_num: int, west_node: str | None = None
    ):
        new_y_top = self.lo.new_layout.domains[north_node].y.min
        if not west_node:
            if col_num == 0:
                new_x_left = self.lo.new_layout.domains[north_node].x.min
            else:
                svlogger.debug(f"No west node, and non 0 col num, North node = {north_node}")
                xl, xr, *_ = self.lo.new_layout.domains[north_node].get_values()
                new_x_left = round((xl + xr) / 2, ROUNDING_LIM)
        else:
            # svlogger.info(f"We have a west node. Its {west_node}")
            new_x_left = self.lo.new_layout.domains[west_node].x.max

        self.create_new_corners(self.lo.curr_node, new_x_left, new_y_top)

    def create_new_corners(self, node: str, new_x_left: Decimal, new_y_top: Decimal):
        dif_x, dif_y = self.calculate_domain_differences(node)

        new_x_max = dif_x + new_x_left
        new_y_min = new_y_top - dif_y

        self.lo.new_layout.domains[node] = Domain.create_domain(
            [new_x_left, new_x_max, new_y_min, new_y_top], node
        )

    def calculate_domain_differences(self, node: str):
        x_min, x_max, y_min, y_max = self.lo.init_layout.domains[node].get_values()

        dif_x = abs(x_max - x_min)
        dif_y = abs(y_max - y_min)

        return dif_x, dif_y
