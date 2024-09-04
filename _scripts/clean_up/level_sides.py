from copy import deepcopy



from svg_helpers.directions import Direction
from svg_helpers.layout import Layout
from svg_helpers.layout_base import LayoutBase
from svg_helpers.shapely import create_box_from_corners

CORNERS_MATCH = {
    Direction.SOUTH: ("y_bottom", min),
    Direction.EAST: ("x_right", max)
}

class SideLeveler(LayoutBase):
    def __init__(self, layout: Layout) -> None:
        super().__init__(deepcopy(layout))

    def run(self):
        for k in CORNERS_MATCH:    
            self.match_to_extreme_val(k)


    def match_to_extreme_val(self, direction):
        vals = []
        relevant_nodes = []
        corner, fx = CORNERS_MATCH[direction]

        for node, data in self.G.nodes(data=True):
            if not data["data"][direction.name]:
                vals.append(self.corners[node][corner])
                relevant_nodes.append(node)

        val = fx(vals)
        for node in relevant_nodes:
            setattr(self.corners[node], corner, val)
            self.shapes[node] = create_box_from_corners(self.corners[node])




