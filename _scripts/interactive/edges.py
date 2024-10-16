from typing import List
import networkx as nx
import typer
from rich import print as rprint
from typing_extensions import Annotated
from interactive.edge_checks import is_valid_assignment
from interactive.edge_helpers import display_edges
from interactive.helpers import (
    CaseNameInput,
    error_print,
    get_edge_details,
    get_subsurfaces,
    write_connectivity_graph,
    write_edges,
)
from interactive.interfaces import SubsurfaceType


def show_edges(case_name: CaseNameInput):
    edge_details = get_edge_details(case_name)
    display_edges(edge_details)

def show_subsurfaces(case_name: CaseNameInput):
    subsurfaces = get_subsurfaces(case_name)
    rprint(subsurfaces)


def assign_connectivity(
    case_name: CaseNameInput,
    n_edges: Annotated[
        List[int], typer.Argument(help="numbers assigned to edges -> run 'show-edges'")
    ],
    undo: Annotated[bool, typer.Option("--undo")] = False,
):
    edge_details = get_edge_details(case_name)
    for i in n_edges:
        if undo:
            edge_details[i].connectivity = False
        else:
            edge_details[i].connectivity = True
    display_edges(edge_details)

    write_edges(case_name, edge_details)


def assign_subsurfaces(
    case_name: CaseNameInput,
    id: Annotated[
        int,
        typer.Argument(help="id of subsurface"),
    ],
    n_edges: Annotated[
        List[int], typer.Argument(help="numbers assigned to edges -> run 'show-edges'")
    ],
    is_window: Annotated[
        bool,
        typer.Option("--window", "-w", help="'WINDOW' if not DOOR"),
    ] = False,
):
    subsurface_type = SubsurfaceType.DOORS if not is_window else SubsurfaceType.DOORS


    subsurfaces = get_subsurfaces(case_name)[subsurface_type.name]
    edge_details = get_edge_details(case_name)
    relevant_edges = [i for i in edge_details if i.ix in n_edges]

    is_valid_assignment(
        id, subsurface_type, subsurfaces, relevant_edges, edge_details, n_edges
    )

    for item in relevant_edges:
        item.detail = id
    write_edges(case_name, edge_details)
    rprint("Result:", relevant_edges)


def save_connectivity_graph(case_name: CaseNameInput):
    edge_details = get_edge_details(case_name)
    Gconn = nx.DiGraph()
    for e in edge_details:
        if e.connectivity:
            if not isinstance(e.detail, int):
                error_print(f"{e} does not have detail assigned!")
            u, v = e.edge
            Gconn.add_edge(u, v, details={"external": e.external, "id": e.detail})

    write_connectivity_graph(case_name, Gconn)
