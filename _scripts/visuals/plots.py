from ast import Index
from itertools import product
import math
from re import sub
from typing import Dict, List
from domains.domain import Domain
import plotly.express as px
import plotly.graph_objects as go

from actions.interfaces import ResultsLog
from plotly.subplots import make_subplots

from fixes.interfaces import Problem


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
    fig,
    domains: Dict[str, Domain],
    row: int,
    col: int,
    label: str,
    xrange=[-1, 12],
    yrange=[-1, 10],
    label_shapes=False,
):
    colors, _ = get_plotly_colors(n_colors=len(domains))
    plot_dict = {}
    for ix, (k, v) in enumerate(domains.items()):
        plot_dict[k] = prepare_shape_dict(v, color=colors[ix])  # type: ignore
        if label_shapes:
            plot_dict[k]["label"] = dict(text=k)

    fig.update_xaxes(
        range=xrange,
        title_text=label,
        title_font=dict(size=10),
        row=row,
        col=col,
    )
    fig.update_yaxes(range=yrange, row=row, col=col)
    for d in plot_dict.values():
        fig.add_shape(**d, row=row, col=col)

    return fig


def make_subplot_indices(n_sols, n_cols=3):
    additional = 1 if (n_sols + 1 % n_cols) > 0 else 0
    n_rows = (n_sols // n_cols) + additional
    print(f"n_rows {n_rows}, n_sols: {n_sols}")
    range_rows = list(range(1, n_rows + 1))
    range_cols = list(range(1, n_cols + 1))
    indices = list(product(range_rows, range_cols))

    print(f"len sols = {n_sols}+1. Len indices = {len(indices)}")
    assert len(indices) >= (n_sols + 1)

    return indices, n_rows, n_cols


def make_subplot_for_all_probs(init_domains, results: List[ResultsLog]):
    indices, n_rows, n_cols = make_subplot_indices(len(results))

    fig = make_subplots(rows=n_rows, cols=n_cols)
    fig = subplot_layout(fig, init_domains, 1, 1, "Init Layout", label_shapes=True)

    for ix, (row, col) in enumerate(indices[1:]):
        try:
            res = results[ix]
            label = f"{ix}.-{res.short_message()}"
            fig = subplot_layout(fig, res.layout.domains, row, col, label)
        except IndexError:
            # out of solutions
            break

    fig.show(renderer="browser")
    return
