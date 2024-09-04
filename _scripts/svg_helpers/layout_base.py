from svg_helpers.layout import Layout


class LayoutBase:
    def __init__(self, layout: Layout) -> None:
        self.G = layout.graph
        self.corners = layout.corners
        self.shapes = layout.shapes
        self.layout  = layout
