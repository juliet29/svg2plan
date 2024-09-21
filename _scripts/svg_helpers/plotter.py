from typing import Dict
from svg_helpers.plots import prepare_shape_dict, get_plotly_colors, plot_shapes
from svg_helpers.domains import DecimalCorners

class Plotter:
    def __init__(self, corners:Dict[str, DecimalCorners], xrange=[-1, 12], yrange=[-1, 8]) -> None:
        self.corners = corners
        self.xrange = xrange
        self.yrange = yrange


    def plot(self):
        colors, _ = get_plotly_colors(n_colors=len(self.corners))

        plot_dict = {}
        for ix, (k, v) in enumerate(self.corners.items()):
                plot_dict[k] = prepare_shape_dict(v, color=colors[ix], label=k) # type: ignore

        fig = plot_shapes(plot_dict, self.xrange, self.yrange)

        fig.show()