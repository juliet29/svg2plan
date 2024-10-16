from os import error
from pathlib import Path
import typer
import json
from rich import print as rprint
from export.save_plan import RoomType
from export.saver import read_pickle, write_pickle
from helpers.layout import Layout
from interactive.interfaces import EdgeDetails, SubSurfacesJSON
from typing_extensions import Annotated

from interactive.subsurface_helpers import open_subsurface_json
import networkx as nx

ROOT_DIR = Path.cwd().parent.parent
OUTPUT_DIR = ROOT_DIR / "outputs2"
SVG_DIR = ROOT_DIR / "svg_imports"


def error_print(m):
    rprint(f"[bold red]{m}[/bold red]")
    raise typer.Exit(code=1)


def complete_case(incomplete: str):
    case_names = [i.name for i in SVG_DIR.glob("*.svg")]
    for name in case_names:
        if name.startswith(incomplete):
            yield (name)
        else:
            return tuple(case_names)


CaseNameInput = Annotated[
    str, typer.Argument(help="case_name", autocompletion=complete_case)
]


class UninitializedSVGError(Exception):
    def __init__(self) -> None:
        error_print("Make sure have 'read-svg' for this case.")
        super().__init__()


def get_case_path(case_name) -> Path:
    return SVG_DIR / case_name


def get_output_path(case_name) -> Path:
    case_path = get_case_path(case_name)
    return OUTPUT_DIR / f"case_{case_path.stem}"


def get_layout(case_name) -> Layout:
    output_path = get_output_path(case_name)
    try:
        return read_pickle(path=(output_path / "layout.pkl"))
    except FileNotFoundError:
        raise UninitializedSVGError


def get_edge_details(case_name) -> list[EdgeDetails]:
    output_path = get_output_path(case_name)
    try:
        return read_pickle(path=(output_path / "edges.pkl"))
    except FileNotFoundError:
        raise UninitializedSVGError


def write_edges(case_name, edge_details):
    output_path = get_output_path(case_name)
    write_pickle(obj=(edge_details), path=(output_path / "edges.pkl"))


def get_subsurfaces(case_name) -> SubSurfacesJSON:
    output_path = get_output_path(case_name)
    try:
        return open_subsurface_json(output_path / "subsurfaces.json")
    except FileNotFoundError:
        raise UninitializedSVGError


def write_subsurfaces(case_name, data):
    output_path = get_output_path(case_name)
    path = output_path / "subsurfaces.json"
    with open(path, "w") as file:
        json.dump(data, default=str, fp=file)


def write_connectivity_graph(case_name, G: nx.Graph):
    G_json = nx.node_link_data(G)
    output_path = get_output_path(case_name)
    path = output_path / "graph.json"
    with open(path, "w+") as file:
        json.dump(G_json, default=str, fp=file)

    rprint(f"Saved connectivity graph to {path.parent / path.name}")


def write_plan(case_name, plan: list[list[RoomType]]):
    output_path = get_output_path(case_name)
    path = output_path / "plan.json"
    with open(path, "w+") as file:
        json.dump(plan, default=str, fp=file)

    rprint(f"Saved floorplan to {path.parent / path.name}")
