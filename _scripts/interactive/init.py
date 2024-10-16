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
    # TODO dont make / save anything until have all info.. 
    pixel_dec = Decimal(pixel_length)
    world_length_dec = create_dimension(world_length).meters
    
    sv = SVGReader(case_path, pixel_dec, world_length_dec)
    sv.run()
    layout = adjust_domains(sv.layout.domains)
    edge_details = init_edge_details(layout)


    output_path = get_output_path(case_name)
    try:
        output_path.mkdir()
    except FileExistsError:
        error_print("Folder already initialized")

    shutil.copy(case_path, output_path)

    subsurfaces_path = output_path / "subsurfaces.json"
    subsurfaces_path.touch(exist_ok=False)


    write_pickle(obj=layout, path=(output_path / "layout.pkl"))
    write_pickle(obj=edge_details, path=(output_path / "edges.pkl"))

    rprint(f"Saved files in '{output_path}'")
