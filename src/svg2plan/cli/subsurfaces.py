import shutil
import sys
from pathlib import Path

sys.path.append(str(Path.cwd().parent))

import typer
from typing_extensions import Annotated

from .helpers import CaseNameInput, get_output_path, get_subsurfaces, write_subsurfaces
from .interfaces import DoorsJSON, DoorType, WindowsJSON, WindowType
from .subsurface_helpers import (
    DimInput,
    complete_wtype,
    create_dimension,
    validate_id,
    validate_wtype,
)


def copy_existing_subsurfaces(case_name: CaseNameInput):
    # TODO optionally copy from another case..
    output_path = get_output_path(case_name)
    def_subsurfaces = Path(output_path.parent / "details" / "subsurfaces.json")
    shutil.copy(def_subsurfaces, output_path)


def create_window(
    case_name: CaseNameInput,
    id: Annotated[int, typer.Argument(help="id")],
    width: Annotated[DimInput, typer.Option("--width", "-w")],
    height: Annotated[DimInput, typer.Option("--height", "-h")],
    head_height: Annotated[DimInput, typer.Option("--head-height", "-hh")],
    opening_height: Annotated[DimInput, typer.Option("--opening-height", "-oh")] = (
        "0",
        "0",
        "0",
    ),
    model: Annotated[str, typer.Option("--model", "-m")] = "Andersen",
    wtype: Annotated[
        str, typer.Option("--wtype", "-wt", autocompletion=complete_wtype)
    ] = "Casement",
    edit: Annotated[bool, typer.Option("--edit")] = False,
):
    existing_data = get_subsurfaces(case_name)
    windows: list[WindowsJSON] = existing_data["WINDOWS"]

    if not edit:
        id = validate_id(windows, id)
    validate_wtype(wtype, opening_height)

    res = WindowType(
        id,
        create_dimension(width),
        create_dimension(height),
        create_dimension(head_height),
        create_dimension(opening_height),
        model,
        wtype,
    )
    # rprint(res)

    windows.append(res.to_json())
    existing_data["WINDOWS"] = windows
    write_subsurfaces(case_name, existing_data)


def create_door(
    case_name: CaseNameInput,
    id: Annotated[int, typer.Argument(help="id")],
    width: Annotated[DimInput, typer.Option("--width", "-w")],
    height: Annotated[DimInput, typer.Option("--height", "-h")],
    thickness: Annotated[DimInput, typer.Option("--thickness", "-t")],
    material: Annotated[str, typer.Option("--model", "-m")] = "SCQC",
    edit: Annotated[bool, typer.Option("--edit")] = False,
):
    existing_data = get_subsurfaces(case_name)
    doors: list[DoorsJSON] = existing_data["DOORS"]

    if not edit:
        id = validate_id(doors, id)

    res = DoorType(
        id,
        create_dimension(width),
        create_dimension(height),
        create_dimension(thickness),
        material,
    )
    # rprint(res)

    doors.append(res.to_json())
    existing_data["DOORS"] = doors
    write_subsurfaces(case_name, existing_data)
