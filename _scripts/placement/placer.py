from placement.interface import LooperInterface
from classes.domains import Corners

class Placer:
    def __init__(self, looper_obj:LooperInterface) -> None:
        self.lo = looper_obj

        # placing nodes
    
    def place_next_south_node(self):
        if not self.lo.tracker[0]:
            # tracker updated AFTER placement
            self.place_north_east_node()
        else:
            north_node = self.lo.tracker[self.lo.tracker_row - 1][0]
            new_y_top = self.lo.domains[north_node].new_corners.y_bottom
            new_x_left = 0

            self.create_new_corners(self.lo.curr_node, new_x_left, new_y_top)



    def place_north_east_node(self):
        assert self.lo.curr_node
        new_x_left = 0
        new_y_top = 0

        self.create_new_corners(self.lo.curr_node, new_x_left, new_y_top)

        print(f"placing north east node - {self.lo.domains[self.lo.curr_node].new_corners}, {self.lo.curr_node}")

    
    def place_next_west_node(self):
        assert self.lo.curr_node
        new_x_left = self.lo.domains[self.lo.curr_node].new_corners.x_right 

        ref_node = self.lo.tracker[self.lo.tracker_row][0]
        new_y_top = self.lo.domains[ref_node].new_corners.y_top

        self.create_new_corners(self.lo.nb, new_x_left, new_y_top)


    


    def calculate_domain_differences(self, node):
        x_left,x_right, y_bottom, y_top = self.lo.domains[node].corners
        dif_x = abs(x_right - x_left)
        dif_y = abs(y_top - y_bottom)

        return dif_x, dif_y


    
    def create_new_corners(self, node, new_x_left, new_y_top):
        dif_x, dif_y = self.calculate_domain_differences(node)

        new_x_right = dif_x + new_x_left
        new_y_bottom = new_y_top - dif_y

        self.lo.domains[node].new_corners = Corners(new_x_left, new_x_right, new_y_bottom, new_y_top)


