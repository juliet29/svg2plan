import sys
sys.path.append("/Users/julietnwagwuume-ezeoke/_UILCode/gqe-phd/svg2plan/_scripts")

from interactive.detail_helpers import (
    DimInput,
    complete_wtype,
    create_dimension,
    open_json,
    update_json,
    validate_id,
    validate_wtype,
)
import typer
from typing_extensions import Annotated
from rich import print as rprint
from interactive.interfaces import DoorType, WindowType


PATH = "test.json"

app = typer.Typer(no_args_is_help=True)


@app.command()
def create_window(
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
    existing_data = open_json(PATH)
    windows: list[dict] = existing_data["WINDOWS"]

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
    rprint(res)

    windows.append(res.to_json())
    existing_data["WINDOWS"] = windows
    update_json(PATH, existing_data)


@app.command()
def create_door(
    id: Annotated[int, typer.Argument(help="id")],
    width: Annotated[DimInput, typer.Option("--width", "-w")],
    height: Annotated[DimInput, typer.Option("--height", "-h")],
    thickness: Annotated[DimInput, typer.Option("--thickness", "-t")],
    material: Annotated[str, typer.Option("--model", "-m")] = "SCQC",
    edit: Annotated[bool, typer.Option("--edit")] = False,
):
    existing_data = open_json(PATH)
    doors: list[dict] = existing_data["DOORS"]

    if not edit:
        id = validate_id(doors, id)

    res = DoorType(
        id,
        create_dimension(width),
        create_dimension(height),
        create_dimension(thickness),
        material,
    )
    rprint(res)

    doors.append(res.to_json())
    existing_data["DOORS"] = doors
    update_json(PATH, existing_data)


@app.callback()
def main(ctx: typer.Context):
    pass


if __name__ == "__main__":
    app()
