from pathlib import Path
import sys
sys.path.append(str(Path.cwd().parent))

from typing import Iterable, List, Literal
import shutil
from typing_extensions import Annotated
from itertools import zip_longest

import typer
from rich import print as rprint

from helpers.layout import Layout
from read.svg_reader import SVGReader
from placement2.attract import adjust_domains
from domains.domain import create_json_doman_dict
from placement2.connectivity import create_cardinal_dags
from export.saver import read_pickle, write_pickle
# from new_solutions.selection import Cook
# from fixes.reporter import Reporter
# from fixes.leveler import level_sides
from rich.console import Console
from rich.table import Table
from helpers.directions import Direction
from helpers.helpers import sort_and_group_objects
from dataclasses import dataclass
from interactive.interfaces import EdgeDetails


ROOT_DIR = Path.cwd().parent.parent
OUTPUT_DIR = ROOT_DIR / "outputs2"
SVG_DIR = ROOT_DIR / "svg_imports"


def complete_case(incomplete: str):
    case_names = [i.name for i in SVG_DIR.glob("*.svg")]
    for name in case_names:
        if name.startswith(incomplete):
            yield (name)
        else:
            return tuple(case_names)




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

def get_output_path(case_name) -> Path:
    case_path = SVG_DIR / case_name
    return OUTPUT_DIR / f"case_{case_path.stem}"

def get_layout(case_name) -> tuple[Layout, list[EdgeDetails]] | None:
    output_path = get_output_path(case_name)
    try:
        return read_pickle(path=(output_path / "layout.pkl"))
    except FileNotFoundError:
        rprint("reading graphs failed. make sure have 'read-svg'.")


CaseNameInput = Annotated[
    str, typer.Argument(help="case_name", autocompletion=complete_case)
]


app = typer.Typer(no_args_is_help=True)


@app.command()
def read_svg(case_name: CaseNameInput):
    case_path = SVG_DIR / case_name
    output_path = OUTPUT_DIR / f"case_{case_path.stem}"

    try:
        output_path.mkdir()
        shutil.copy(case_path, output_path / case_name)
    except FileExistsError:
        print("Folder already initialized")

    sv = SVGReader(case_name)  # TODO pass dimensions..
    # pixel_length: int, true_length: tuple[str, str, str]
    sv.run()
    domains, graphs = adjust_domains(sv.layout.domains)
    layout = Layout(domains, graphs)
    edge_details = init_edge_details(graphs)

    write_pickle(obj=(layout, edge_details), path=(output_path / "layout.pkl"))

    rprint(f"Saved files in '{output_path}'")


def stringify(ix, e):
    if e:
        u, v = e
        return f"{ix}.({u} - {v})"
    else:
        return ""
    
def prepare(edge_details: Iterable[EdgeDetails] | None):

    if edge_details:
        return [stringify(i.ix, i.edge) for i in edge_details]
    else: 
        return []

def display_edges(edge_details):
    table = Table(title="Edges")
    table.add_column("Adjacency", style="cyan")
    table.add_column("Connectivity", style="magenta")

    x_conn = prepare(filter(lambda i: i.connectivity and i.axis=="x", edge_details))
    y_conn =prepare( filter(lambda i: i.connectivity and i.axis=="y", edge_details))
    x_adj = prepare(filter(lambda i: not i.connectivity and i.axis=="x", edge_details))
    y_adj = prepare(filter(lambda i: not i.connectivity and i.axis=="y", edge_details))


    for adj, conn in zip_longest(x_adj, x_conn):
        table.add_row(adj, conn)

    table.add_section()

    for adj, conn in zip_longest(y_adj, y_conn):
        table.add_row(adj, conn)

    console = Console()
    console.print(table)



@app.command()
def show_edges(case_name: CaseNameInput):
    layout = get_layout(case_name)
    if not layout:
        return
    *_, edge_details = layout
    display_edges(edge_details)


@app.command()
def assign_connectivity(
    case_name: CaseNameInput,
    n_edges: Annotated[
        List[int], typer.Argument(help="numbers assigned to edges -> run 'show-edges'")
    ],
    undo: Annotated[bool, typer.Option("--undo")] = False, 
):
    res = get_layout(case_name)
    if not res:
        return
    *layout, edge_details= res


    for i in n_edges:
        if undo:
            edge_details[i].connectivity = False
        else:
            edge_details[i].connectivity = True

    display_edges(edge_details)

    output_path = get_output_path(case_name)
    write_pickle(obj=(layout, edge_details), path=(output_path / "layout.pkl"))
    
@app.command()
def reset_connectivity(case_name: CaseNameInput):
    res = get_layout(case_name)
    if not res:
        return
    *layout, edge_details= res
    for i in edge_details:
            i.connectivity = False

    display_edges(edge_details)

    output_path = get_output_path(case_name)
    write_pickle(obj=(layout, edge_details), path=(output_path / "layout.pkl"))






# # maybe this is a bash script..
# def clean_up_layout(case_name: CaseNameInput):
#     layout = get_layout(case_name)
#     if not layout:
#         return
#     c = Cook(Reporter(layout))
#     # TODO do a while loop with checks..

#     # TODO take the layout object
#     leveled_domains = level_sides(layout.graphs, layout.domains)


@app.callback()
def main(ctx: typer.Context):
    pass


if __name__ == "__main__":
    app()
