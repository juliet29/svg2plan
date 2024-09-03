from typing import Dict
from svg_helpers.plots import prepare_shape_dict, get_plotly_colors, plot_shapes
from classes.domains import Corners

class Plotter:
    def __init__(self, corners:Dict[str, Corners]) -> None:
        self.corners = corners

    def plot(self):
        colors, _ = get_plotly_colors(n_colors=len(self.corners))

        plot_dict = {}
        for ix, (k, v) in enumerate(self.corners.items()):
                plot_dict[k] = prepare_shape_dict(v, color=colors[ix], label=k) # type: ignore

        fig = plot_shapes(plot_dict, x_range=[-10, 800], y_range=[-600, 10])

        fig.show()