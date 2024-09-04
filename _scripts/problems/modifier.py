from shapely import box
from copy import deepcopy
from problems.classes.actions import Action, ActionType
from svg_helpers.layout_base import LayoutBase
from svg_helpers.layout import Layout
from svg_helpers.shapely import create_box_from_corners


class BlockModifier(LayoutBase):
    def __init__(self, action: Action, layout: Layout) -> None:
        super().__init__(deepcopy(layout))
        # self.shapes = deepcopy(layout.shapes)
        # self.corners = deepcopy(layout.corners)
        # self.G = layout.graph

        self.curr_polygon = self.shapes[action.node]
        self.curr_corners = self.corners[action.node]
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
        self.shapes[self.node] = create_box_from_corners(self.curr_corners)

    def push(self):
        # to the right
        self.curr_corners.x_right += self.distance
        self.curr_corners.x_left += self.distance
        self.shapes[self.node] = create_box_from_corners(self.curr_corners)

    def get_modified_layout(self):
        self.modified_layout = Layout(self.shapes, self.corners, self.G)
        return self.modified_layout
