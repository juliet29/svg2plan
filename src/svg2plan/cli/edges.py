import networkx as nx
from rich import print as rprint
from .edge_helpers import display_edges
from .helpers import (
    SVGNameInput,
    error_print,
    get_edge_details,
    get_subsurfaces,
    write_connectivity_graph,
    write_edges,
)


def show_edges(case_name: SVGNameInput):
    edge_details = get_edge_details(case_name)
    display_edges(edge_details)


def show_subsurfaces(case_name: SVGNameInput):
    subsurfaces = get_subsurfaces(case_name)
    rprint(subsurfaces)


def assign_remaining_subsurfaces(case_name: SVGNameInput):
    edge_details = get_edge_details(case_name)
    for e in edge_details:
        if e.connectivity and not isinstance(e.detail, int):
            e.detail = 1
    write_edges(case_name, edge_details)
    rprint("assigned remaining subsurfaces ")


def save_connectivity_graph(case_name: SVGNameInput):
    edge_details = get_edge_details(case_name)
    Gconn = nx.DiGraph()
    for e in edge_details:
        if e.connectivity:
            if not isinstance(e.detail, int):
                error_print(f"{e} does not have detail assigned!")
            u, v = e.edge
            Gconn.add_edge(u, v, details={"external": e.external, "id": e.detail})

    write_connectivity_graph(case_name, Gconn)
