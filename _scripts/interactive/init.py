from export.saver import write_pickle
from helpers.layout import Layout
from interactive.edge_helpers import init_edge_details
from interactive.helpers import CaseNameInput, error_print, get_case_path, get_output_path
from interactive.subsurface_helpers import DimInput, create_dimension
from placement.attract import adjust_domains
from svg_reader import SVGReader


import typer
from rich import print as rprint


import shutil
from decimal import Decimal
from typing_extensions import Annotated

INIT_WORLD_LEN = ("10", "6", "3/4")
INIT_PX_LEN = "234"


def init(
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
        error_print("Folder already initialized")

    shutil.copy(case_path, output_path)
    subsurfaces_path.touch(exist_ok=False)

    pixel_dec = Decimal(pixel_length)
    world_length_dec = create_dimension(world_length).meters
    sv = SVGReader(case_path, pixel_dec, world_length_dec)
    sv.run()
    domains, graphs = adjust_domains(sv.layout.domains)
    layout = Layout(domains, graphs)
    edge_details = init_edge_details(graphs)

    write_pickle(obj=layout, path=(output_path / "layout.pkl"))
    write_pickle(obj=edge_details, path=(output_path / "edges.pkl"))

    rprint(f"Saved files in '{output_path}'")
