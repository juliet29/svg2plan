from typing import Dict
from visuals.plots import prepare_shape_dict, get_plotly_colors, plot_shapes
from domains.domain import Domain


class Plotter:
    def __init__(
        self, domains: Dict[str, Domain], xrange=[-1, 12], yrange=[-10, 10], title: str = ""
    ) -> None:
        self.domains = domains
        self.xrange = xrange
        self.yrange = yrange
        self.title = title

    def plot(self):
        colors, _ = get_plotly_colors(n_colors=len(self.domains))

        plot_dict = {}
        for ix, (k, v) in enumerate(self.domains.items()):
            plot_dict[k] = prepare_shape_dict(v, color=colors[ix], label=k)  # type: ignore

        fig = plot_shapes(plot_dict, self.xrange, self.yrange)
        fig.update_layout(title=self.title)

        fig.show()


def plot_general(domains: Dict[str, Domain], title:str=""):
    plt = Plotter(domains, title=title)
    plt.plot()