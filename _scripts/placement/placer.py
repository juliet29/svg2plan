import logging
from placement.interface import LooperInterface
from svg_helpers.constants import ROUNDING_LIM
from svg_helpers.domains import Corners, DecimalCorners, empty_decimal_corner
from svg_helpers.decimal_operations import decimal_mult, decimal_add, decimal_sub
from decimal import Decimal

logger = logging.getLogger(__name__)

class Placer:
    def __init__(self, looper_obj: LooperInterface) -> None:
        self.lo = looper_obj

    def place_north_west_node(self):
        new_x_left = Decimal(0)
        new_y_top = Decimal(0)
        self.create_new_corners(self.lo.curr_node, new_x_left, new_y_top)

    def place_next_east_node(self, west_node):
        new_y_top = Decimal(0)
        new_x_left = self.lo.new_domains.corners[west_node].x_right
        self.create_new_corners(self.lo.curr_node, new_x_left, new_y_top)

    def place_next_south_node(self, north_node, west_node=None):
        new_y_top = self.lo.new_domains.corners[north_node].y_bottom
        if not west_node:
            new_x_left = self.lo.new_domains.corners[north_node].x_left
        else:
            if self.lo.new_domains.corners[west_node] == empty_decimal_corner:
                xl, xr, *_ = self.lo.new_domains.corners[north_node]
                new_x_left = round((xl + xr) / 2, ROUNDING_LIM)
                logger.debug(
                    f"{west_node}, the east node of {self.lo.curr_node} has not yet been placed. Creating a new x_left at {new_x_left}"
                )
            else:
                new_x_left = self.lo.new_domains.corners[west_node].x_right
            

        self.create_new_corners(self.lo.curr_node, new_x_left, new_y_top)

    def create_new_corners(self, node, new_x_left, new_y_top):
        dif_x, dif_y = self.calculate_domain_differences(node)

        new_x_right = dif_x + new_x_left
        new_y_bottom = new_y_top - dif_y

        self.lo.new_domains.corners[node] = DecimalCorners(
            new_x_left, new_x_right, new_y_bottom, new_y_top
        )

    def calculate_domain_differences(self, node):
        x_left, x_right, y_bottom, y_top = self.lo.init_layout.corners[node]

        dif_x = abs(x_right - x_left)
        dif_y = abs(y_top - y_bottom)

        return dif_x, dif_y
