from itertools import zip_longest
from typing import Iterable
from rich.console import Console
from rich.table import Table
from helpers.directions import Direction
from helpers.helpers import sort_and_group_objects
from interactive.helpers import EdgeDetails
from placement.cardinal import create_cardinal_dags


def number_edges(G, ax, start=0):
    drns = [i.name for i in Direction]
    g1, g2 = sort_and_group_objects(G.edges, fx=lambda x: x[0] in drns or x[1] in drns)
    g1e = [EdgeDetails(start + i, e, ax) for i, e in enumerate(g1)]
    g2e = [
        EdgeDetails(start + len(g1e) + i, e, ax, external=True)
        for i, e in enumerate(g2)
    ]
    return g1e + g2e


def init_edge_details(graphs):
    Gxc, Gyc = create_cardinal_dags(*graphs)
    x_assign = number_edges(Gxc, ax="x")
    y_assign = number_edges(Gyc, ax="y", start=len(x_assign))
    return x_assign + y_assign


def stringify(ix, e):
    u, v = e
    return f"{ix}.({u} - {v})"


def stringify_with_detail(ix, e, d):
    u, v = e
    return f"{ix}.({u} - {v}) ({d})"


def prepare(edge_details: Iterable[EdgeDetails] | None):
    res = []
    if edge_details:
        for i in edge_details:
            if not isinstance(i.detail, int):
                res.append(stringify(i.ix, i.edge))
            else:
                res.append(stringify_with_detail(i.ix, i.edge, i.detail))
        return res
    else:
        return []


def display_edges(edge_details):
    table = Table(title="Edges")
    table.add_column("Adjacency", style="cyan")
    table.add_column("Connectivity", style="magenta")

    x_conn = prepare(filter(lambda i: i.connectivity and i.axis == "x", edge_details))
    y_conn = prepare(filter(lambda i: i.connectivity and i.axis == "y", edge_details))
    x_adj = prepare(
        filter(lambda i: not i.connectivity and i.axis == "x", edge_details)
    )
    y_adj = prepare(
        filter(lambda i: not i.connectivity and i.axis == "y", edge_details)
    )

    for adj, conn in zip_longest(x_adj, x_conn):
        table.add_row(adj, conn)

    table.add_section()

    for adj, conn in zip_longest(y_adj, y_conn):
        table.add_row(adj, conn)

    console = Console()
    console.print(table)
