from shapely import box
from copy import deepcopy
from problems.classes.actions import Action, ActionType
from classes.layout import Layout
from svg_helpers.shapely import create_polygon_from_corners


class ModifyBlock:
    def __init__(self, action: Action, layout: Layout) -> None:
        self.all_shapes = deepcopy(layout.shapes)
        self.all_corners = deepcopy(layout.corners)
        self.graph = layout.graph

        self.curr_polygon = self.all_shapes[action.node]
        self.curr_corners = self.all_corners[action.node]
        self.distance = action.distance
        self.node = action.node
        self.action = action

    def run(self):
        if self.action.action_type == ActionType.STRETCH:
            self.stretch()
        elif self.action.action_type == ActionType.PUSH:
            self.push()
        self.get_modified_layout()

    def stretch(self):
        # to the right 
        self.curr_corners.x_right += self.distance
        self.all_shapes[self.node] = create_polygon_from_corners(self.curr_corners)

    def push(self):
        # to the right 
        self.curr_corners.x_right += self.distance
        self.curr_corners.x_left += self.distance
        self.all_shapes[self.node] = create_polygon_from_corners(self.curr_corners)

    def get_modified_layout(self):
        self.modified_layout = Layout(self.all_shapes, self.all_corners, self.graph)
        return self.modified_layout



