import shutil
from decimal import Decimal

import typer
from rich import print as rprint
from typing_extensions import Annotated

from svg2plan.cli.helpers import remove_files
from svg2plan.helpers.utils import get_curr_datetime

from ..constants import BASE_PATH, INIT_PX_LEN, INIT_WORLD_LEN
from ..helpers.save import write_pickle
from ..placement.attract import adjust_domains
from ..svg_reader import SVGReader
from .edge_helpers import init_edge_details
from .helpers import (
    SVGNameInput,
    error_print,
    get_svg_path,
    get_output_path,
)
from .subsurface_helpers import DimInput, create_dimension


SAVED_ADJ_DIR = BASE_PATH / "saved_adjacencies"


def save_existing_connectivity_data(output_path, case_path):
    edges_pkl = output_path / "edges.pkl"
    rprint("")
    save_adj_path = SAVED_ADJ_DIR / case_path.stem
    if not save_adj_path.exists():
        save_adj_path.mkdir()
    new_edges_pkl = save_adj_path / f"edges_{get_curr_datetime()}.pkl"
    shutil.copy(edges_pkl, new_edges_pkl)
    rprint(f"Copied edges (and connectivity data) to `{new_edges_pkl}`")


def init(
    svg_name: SVGNameInput,
    pixel_length: Annotated[str, typer.Argument(help="pixel len")] = INIT_PX_LEN,
    world_length: Annotated[DimInput, typer.Argument(help="real len")] = INIT_WORLD_LEN,
    reset: Annotated[bool, typer.Option(help="Overwrite existing folder")] = False,
):
    svg_path = get_svg_path(svg_name)

    pixel_dec = Decimal(pixel_length)
    world_dim = create_dimension(world_length)

    sv = SVGReader(svg_path, pixel_dec, world_dim.meters)
    sv.run()
    layout = adjust_domains(sv.domains)
    edge_details = init_edge_details(layout)

    output_path = get_output_path(svg_name)
    try:
        output_path.mkdir()
    except FileExistsError:
        if reset:
            save_existing_connectivity_data(output_path, svg_path)
            remove_files(output_path)
        else:
            error_print("Folder already initialized. Add `--reset` flag to overwrite")

    # copy svg to case
    shutil.copy(svg_path, output_path)

    # write dimensions in config..
    (output_path / "config.txt").write_text(
        f"{pixel_length}px -> {world_dim}", encoding="utf-8"
    )

    # create path for subsurfaces
    subsurfaces_path = output_path / "subsurfaces.json"
    subsurfaces_path.touch(exist_ok=False)

    # save temp data, layout + edges
    write_pickle(obj=layout, path=(output_path / "layout.pkl"))
    write_pickle(obj=edge_details, path=(output_path / "edges.pkl"))

    rprint(f"Saved files in `{output_path}`")
