import shutil
from decimal import Decimal

import typer
from rich import print as rprint
from typing_extensions import Annotated

from ..constants import INIT_PX_LEN, INIT_WORLD_LEN
from ..helpers.save import write_pickle
from ..placement.attract import adjust_domains
from ..svg_reader import SVGReader
from .edge_helpers import init_edge_details
from .helpers import (
    CaseNameInput,
    error_print,
    get_case_path,
    get_output_path,
)
from .subsurface_helpers import DimInput, create_dimension


def init(
    case_name: CaseNameInput,
    pixel_length: Annotated[str, typer.Argument(help="pixel len")] = INIT_PX_LEN,
    world_length: Annotated[DimInput, typer.Argument(help="real len")] = INIT_WORLD_LEN,
):
    case_path = get_case_path(case_name)
    # TODO dont make / save anything until have all info..
    pixel_dec = Decimal(pixel_length)
    world_dim = create_dimension(world_length)


    sv = SVGReader(case_path, pixel_dec, world_dim.meters)
    sv.run()
    layout = adjust_domains(sv.domains)
    edge_details = init_edge_details(layout)

    output_path = get_output_path(case_name)
    try:
        output_path.mkdir()
    except FileExistsError:
        error_print("Folder already initialized")

    # copy svg to case 
    shutil.copy(case_path, output_path)

    # write dimensions in config.. 
    (output_path / "config.txt").write_text(f"{pixel_length}px -> {world_dim}", encoding="utf-8")

    # create path for subsurfaces 
    subsurfaces_path = output_path / "subsurfaces.json"
    subsurfaces_path.touch(exist_ok=False)

    # save temp data, layout + edges 
    write_pickle(obj=layout, path=(output_path / "layout.pkl"))
    write_pickle(obj=edge_details, path=(output_path / "edges.pkl"))

    rprint(f"Saved files in '{output_path}'")


