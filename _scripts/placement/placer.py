from placement.interface import LooperInterface
from svg_helpers.domains import Corners
from svg_helpers.decimal_operations import decimal_mult, decimal_add, decimal_sub





class Placer:
    def __init__(self, looper_obj:LooperInterface) -> None:
        self.lo = looper_obj

    def place_north_west_node(self):
        new_x_left = 0
        new_y_top = 0
        self.create_new_corners(self.lo.curr_node, new_x_left, new_y_top)

    
    def place_next_east_node(self, west_node):
        new_y_top = 0
        new_x_left = self.lo.domains[west_node].new_corners.x_right 
        self.create_new_corners(self.lo.curr_node, new_x_left, new_y_top)


    def place_next_south_node(self, north_node, west_node):
        new_y_top = self.lo.domains[north_node].new_corners.y_bottom
        if west_node:
            if self.lo.domains[west_node].new_corners == Corners(0,0,0,0):
                print(f"{west_node}, the east node of {self.lo.curr_node} has not yet been placed.")
                xl, xr, *_ =  self.lo.domains[north_node].new_corners
                new_x_left = decimal_add(xl, xr)/2
            else:
                new_x_left = self.lo.domains[west_node].new_corners.x_right
        else:
            new_x_left = self.lo.domains[north_node].new_corners.x_left

        self.create_new_corners(self.lo.curr_node, new_x_left, new_y_top)


    def create_new_corners(self, node, new_x_left, new_y_top):
        dif_x, dif_y = self.calculate_domain_differences(node)

        new_x_right = decimal_add(dif_x, new_x_left)
        new_y_bottom = decimal_sub(new_y_top, dif_y)

        self.lo.domains[node].new_corners = Corners(new_x_left, new_x_right, new_y_bottom, new_y_top)

    def calculate_domain_differences(self, node):
        x_left, x_right, y_bottom, y_top = self.lo.domains[node].corners


        dif_x = abs(decimal_sub(x_right, x_left))
        dif_y = abs(decimal_sub(y_top, y_bottom))

        return dif_x, dif_y



