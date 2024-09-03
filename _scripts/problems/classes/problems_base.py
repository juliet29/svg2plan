from classes.layout import Layout

class ProblemsBase:
    def __init__(self, layout:Layout) -> None:
        self.G = layout.graph
        self.corners = layout.corners
        self.shapes = layout.shapes