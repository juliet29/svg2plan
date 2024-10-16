from decimal import Decimal
from pathlib import Path
import sys
sys.path.append(str(Path.cwd().parent))


from typing import Iterable, List
import shutil
from typing_extensions import Annotated

import typer
from rich import print as rprint
import networkx as nx

from helpers.layout import Layout
from read.svg_reader import SVGReader
from placement2.attract import adjust_domains
from export.saver import read_pickle, write_pickle
from interactive.helpers import (
    get_case_path,
    get_edge_details,
    get_output_path,
    get_layout,
    CaseNameInput,
    get_subsurfaces,
    write_connectivity_graph,
    write_edges,
)
from interactive.edge_helpers import display_edges, init_edge_details
from interactive.interfaces import SubsurfaceType
from interactive.subsurface_helpers import create_dimension, DimInput

INIT_WORLD_LEN = ("10", "6", "3/4")
INIT_PX_LEN = "234"

app = typer.Typer(no_args_is_help=True, pretty_exceptions_show_locals=False)


@app.command()
def read_svg(
    case_name: CaseNameInput,
    pixel_length: Annotated[str, typer.Argument(help="pixel len")] = INIT_PX_LEN,
    world_length: Annotated[DimInput, typer.Argument(help="real len")] = INIT_WORLD_LEN,
):
    case_path = get_case_path(case_name)
    output_path = get_output_path(case_name)
    subsurfaces_path = output_path / "subsurfaces.json"

    try:
        output_path.mkdir()
    except FileExistsError:
        print("Folder already initialized")
        return

    shutil.copy(case_path, output_path)
    subsurfaces_path.touch(exist_ok=False)

    pixel_dec = Decimal(pixel_length)
    world_length_dec = create_dimension(world_length).meters
    sv = SVGReader(case_name, pixel_dec, world_length_dec)
    sv.run()
    domains, graphs = adjust_domains(sv.layout.domains)
    layout = Layout(domains, graphs)
    edge_details = init_edge_details(graphs)

    write_pickle(obj=layout, path=(output_path / "layout.pkl"))
    write_pickle(obj=edge_details, path=(output_path / "edges.pkl"))

    rprint(f"Saved files in '{output_path}'")


@app.command()
def show_edges(case_name: CaseNameInput):
    edge_details = get_edge_details(case_name)
    display_edges(edge_details)


@app.command()
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


@app.command()
def reset_connectivity(case_name: CaseNameInput):
    edge_details = get_edge_details(case_name)
    for i in edge_details:
        i.connectivity = False

    display_edges(edge_details)
    write_edges(case_name, edge_details)


@app.command()
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


@app.command()
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



@app.callback()
def main(ctx: typer.Context):
    pass


if __name__ == "__main__":
    app()
