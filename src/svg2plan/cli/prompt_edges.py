from copy import deepcopy
import typer
from .edge_checks import is_valid_id
from .helpers import (
    SVGNameInput,
    get_edge_details,
    get_subsurfaces,
    write_edges,
)
from .edge_helpers import (
    ask_about_connected_edges,
    ask_about_edges_for_subsurface,
    display_edges,
)
from typing import Annotated
from beaupy import confirm
from ..helpers.utils import chain_flatten
from .interfaces import SubsurfaceType
from rich import print as rprint


def reset_edge_details(case_name: SVGNameInput):
    _edge_details = get_edge_details(case_name)
    edge_details = deepcopy(_edge_details)
    for i in edge_details:
        i.connectivity = False
        i.detail = None

    display_edges(edge_details)
    if confirm("Are you sure you want to clear edges?"):
        write_edges(case_name, edge_details)
    else:
        rprint("Abandoning changes...")


def assign_connectivity(svg_name: SVGNameInput):
    _edge_details = get_edge_details(svg_name)
    edge_details = deepcopy(_edge_details)

    pairs = [
        ("x", False),
        ("x", True),
        ("y", False),
        ("y", True),
    ]

    edge_ids = []
    for pair in pairs:
        selected_ids = ask_about_connected_edges(edge_details, *pair)
        edge_ids.append(selected_ids)
    edge_ids = chain_flatten(edge_ids)
    rprint(f"Selected edges: {edge_ids}")

    for i in edge_ids:
        edge_details[i].connectivity = True

    display_edges(edge_details)
    if confirm("Are the edges correct?"):
        write_edges(svg_name, edge_details)
    else:
        rprint("Abandoning changes...")

    rprint(f"Completed work on {svg_name}")


# TOD possibly unassign connectivity with undo flag..


def assign_subsurfaces(
    svg_name: SVGNameInput,
    id: Annotated[
        int,
        typer.Argument(help="id of subsurface"),
    ],
    is_window: Annotated[
        bool,
        typer.Option("--window", "-w", help="'WINDOW' if not DOOR"),
    ] = False,
):
    _edge_details = get_edge_details(svg_name)
    edge_details = deepcopy(_edge_details)

    subsurface_type = SubsurfaceType.DOORS if not is_window else SubsurfaceType.WINDOWS

    subsurfaces = get_subsurfaces(svg_name)[subsurface_type.name]
    is_valid_id(subsurfaces, id)

    edge_details = get_edge_details(svg_name)
    axes = ["x", "y"]

    edge_ids = []
    for ax in axes:
        selected_ids = ask_about_edges_for_subsurface(
            edge_details, ax, id, subsurface_type.name
        )
        edge_ids.append(selected_ids)
    edge_ids = chain_flatten(edge_ids)
    rprint(f"Selected edges: {edge_ids}")

    for i in edge_ids:
        edge_details[i].detail = id

    display_edges(edge_details)
    if confirm("Are the edges correct?"):
        write_edges(svg_name, edge_details)
    else:
        rprint("Abandoning changes...")

    rprint(f"Completed work on {svg_name}")
