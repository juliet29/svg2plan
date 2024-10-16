from typing import List
import networkx as nx
import typer
from rich import print as rprint
from typing_extensions import Annotated
from interactive.edge_helpers import display_edges
from interactive.helpers import (
    CaseNameInput,
    get_edge_details,
    get_subsurfaces,
    write_connectivity_graph,
    write_edges,
)
from interactive.interfaces import SubsurfaceType


def show_edges(case_name: CaseNameInput):
    edge_details = get_edge_details(case_name)
    display_edges(edge_details)


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
    subsurface_type: Annotated[
        SubsurfaceType,
        typer.Argument(help="'WINDOW' if not DOOR"),
    ] = SubsurfaceType.DOORS,
):
    all_subsurfaces = get_subsurfaces(case_name)
    subsurfaces = all_subsurfaces[subsurface_type.name]
    rprint(subsurfaces)
    edge_details = get_edge_details(case_name)
    relevant_edges = [i for i in edge_details if i.ix in n_edges]
    rprint("Before", relevant_edges)

    # TODO typer errors.. and make into fx
    valid_ids = [item["id"] for item in subsurfaces]
    assert id in valid_ids, "Invalid ID"

    edges_types = [i.external for i in relevant_edges]
    assert len(set(edges_types)) == 1, "Should only have one kind of edge"
    if subsurface_type == SubsurfaceType.DOORS:
        assert (
            all(edges_types) == False
        ), f"Should only have internal edges for subsurface type {subsurface_type}"
    else:
        assert (
            all(edges_types) == True
        ), f"Should only have external edges for subsurface type {subsurface_type}"

    connectivity_edges = set([item.ix for item in edge_details if item.connectivity])
    assert set(n_edges) <= connectivity_edges, "Edges are not connectivity edges"

    # passes checks, assign edges..
    for item in relevant_edges:
        item.detail = id

    write_edges(case_name, edge_details)

    rprint("\nAfter", relevant_edges)


def save_connectivity_graph(case_name: CaseNameInput):

    edge_details = get_edge_details(case_name)

    # check all have detal assigned

    Gconn = nx.DiGraph()
    for e in edge_details:
        if e.connectivity:
            if not isinstance(e.detail, int):
                raise Exception(f"{e} does not have detail assigned!")
            u, v = e.edge
            Gconn.add_edge(u, v, details={"external": e.external, "id": e.detail})

    write_connectivity_graph(case_name, Gconn)
