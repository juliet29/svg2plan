from itertools import zip_longest
from typing import Iterable, List
from ..helpers.directions import Direction
from ..helpers.utils import sort_and_group_objects
from ..helpers.layout import Layout
from .interfaces import EdgeDetails
from ..placement.cardinal import create_cardinal_dags

from rich.console import Console
from rich.table import Table
from beaupy import select_multiple

STYLE = "cyan1 bold"


def number_edges(G, ax, start=0):
    drns = [i.name for i in Direction]
    g1, g2 = sort_and_group_objects(G.edges, fx=lambda x: x[0] in drns or x[1] in drns)
    g1e = [EdgeDetails(start + i, e, ax) for i, e in enumerate(g1)]
    g2e = [
        EdgeDetails(start + len(g1e) + i, e, ax, external=True)
        for i, e in enumerate(g2)
    ]
    return g1e + g2e


def init_edge_details(layout: Layout):
    Gxc, Gyc = create_cardinal_dags(layout)
    x_assign = number_edges(Gxc, ax="x")
    y_assign = number_edges(Gyc, ax="y", start=len(x_assign))
    return x_assign + y_assign


def filter_ax_and_external(edge_details: list[EdgeDetails], axis: str, external: bool):
    return list(
        filter(lambda i: i.external == external and i.axis == axis, edge_details)
    )


def filter_ax_and_connectivity(
    edge_details: list[EdgeDetails], axis: str, connectivity: bool
):
    return list(
        filter(
            lambda i: i.connectivity == connectivity and i.axis == axis, edge_details
        )
    )


def get_edge_strings(edge_details: Iterable[EdgeDetails]):
    return [f"{i!s}" for i in edge_details]


def display_edges(edge_details: list[EdgeDetails]):
    table = Table(title="Edges")
    table.add_column("Adjacency", style="cyan")
    table.add_column("Connectivity", style="magenta")

    pairs = [("x", False), ("x", True), ("y", False), ("y", True)]
    x_adj, x_conn, y_adj, y_conn = [
        get_edge_strings(filter_ax_and_connectivity(edge_details, *p)) for p in pairs
    ]

    for adj, conn in zip_longest(x_adj, x_conn):
        table.add_row(adj, conn)

    table.add_section()

    for adj, conn in zip_longest(y_adj, y_conn):
        table.add_row(adj, conn)

    console = Console()
    console.print(table)

    return table


def get_edges_for_prompt(
    edge_details: list[EdgeDetails], axis: str, external: bool, subsurfaces=True
) -> tuple[Iterable[EdgeDetails], List[str]]:
    if subsurfaces:
        edges = filter_ax_and_connectivity(edge_details, axis, True)
    else:
        edges = filter_ax_and_external(edge_details, axis, external)
    strings = get_edge_strings(edges)

    return edges, strings


def ask_about_connected_edges(
    edge_details: list[EdgeDetails], axis: str, external: bool
) -> list[int]:
    console = Console()
    edges, strings = get_edges_for_prompt(edge_details, axis, external, False)

    ticked_indices = [ix for ix, e in enumerate(edges) if e.connectivity]

    location = "Exterior" if external else "Interior"
    console.print(f"[{axis.upper()} {location}] Which edges are connected?")

    items = select_multiple(
        strings,
        return_indices=True,
        ticked_indices=ticked_indices,
        tick_style=STYLE,
        cursor_style=STYLE,
    )  # type: ignore

    return [e.ix for ix, e in enumerate(edges) if ix in items]


def ask_about_edges_for_subsurface(
    edge_details: list[EdgeDetails], axis: str, s_id: int, stype: str
) -> list[int]:
    console = Console()
    edges, strings = get_edges_for_prompt(edge_details, axis, True, True)

    if not edges:
        print(f"No connected edges in {axis.upper()} ")
        return []

    console.print(f"Select {axis.upper()} edges for {stype} type {s_id}")

    items = select_multiple(
        strings, return_indices=True, tick_style=STYLE, cursor_style=STYLE
    )  # type: ignore

    return [e.ix for ix, e in enumerate(edges) if ix in items]
