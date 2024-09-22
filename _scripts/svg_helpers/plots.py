# from svg_helpers.domains import Domain, Corners
from new_corners.domain import Domain
import plotly.express as px
import plotly.graph_objects as go


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


def get_plotly_colors(n_colors=10, color_scheme="turbo"):
    colors = px.colors.sample_colorscale(
        color_scheme, 
        [n / (n_colors - 1) for n in range(n_colors)]
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
