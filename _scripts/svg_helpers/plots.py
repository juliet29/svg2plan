# from svg_helpers.domains import Domain, Corners
from ast import Index
from itertools import product
import math
from typing import Dict
from new_corners.domain import Domain
import plotly.express as px
import plotly.graph_objects as go

from new_solutions.interfaces import ResultsLog
from plotly.subplots import make_subplots


def prepare_shape_dict(
    domain: Domain,
    type="rect",
    color="blue",
    label="",
):
    d = dict(
        type=type,
        xref="x",
        yref="y",
        fillcolor=color,
        x0=domain.x.min,
        y0=domain.y.min,
        x1=domain.x.max,
        y1=domain.y.max,
        label=dict(text=label),
        opacity=0.5,
    )

    return d


def test():
    return 4


def get_plotly_colors(n_colors=10, color_scheme="turbo"):
    colors = px.colors.sample_colorscale(
        color_scheme, [n / (n_colors - 1) for n in range(n_colors)]
    )
    return colors, iter(colors)


def plot_shapes(plot_dict, x_range=[-10, 300], y_range=[-300, 10]):
    fig = go.Figure()
    for trace in plot_dict.values():
        fig.add_shape(**trace)

    fig.update_xaxes(range=x_range)
    fig.update_yaxes(range=y_range)

    fig_width = 800
    fig_height = 480
    padding = 50

    fig.update_layout(
        autosize=False,
        width=fig_width,
        height=fig_height,
        margin=dict(l=padding, r=padding, b=padding, t=padding, pad=4),
    )

    return fig


def subplot_layout(
    fig, domains: Dict[str, Domain], row, col, xrange=[-1, 12], yrange=[-10, 1]
):
    colors, _ = get_plotly_colors(n_colors=len(domains))
    plot_dict = {}
    for ix, (k, v) in enumerate(domains.items()):
        plot_dict[k] = prepare_shape_dict(v, color=colors[ix])  # type: ignore

    fig.update_xaxes(range=xrange, row=row, col=col)
    fig.update_yaxes(range=yrange, row=row, col=col)
    for d in plot_dict.values():
        fig.add_shape(**d, row=row, col=col)

    return fig


def get_subplot_index(num_sols):
    n_rows = math.ceil(math.sqrt(num_sols))
    range_rows = list(range(n_rows))
    indices = list(product(range_rows, range_rows))

    return indices, n_rows


def make_subplot_for_results(results: list[ResultsLog]):
    num_sols = len(results)
    indices, n_rows = get_subplot_index(num_sols)
    assert len(indices) >= num_sols
    print(f"len sols = {num_sols}. Len indices = {len(indices)}")

    fig = make_subplots(rows=n_rows, cols=n_rows)
    for ix, (row, col) in enumerate(indices):
        # print(ix, (row, col))
        try:
            fig = subplot_layout(fig, results[ix].domains, row + 1, col + 1)
        except IndexError:
            # out of solutions to print...
            pass

    return fig
