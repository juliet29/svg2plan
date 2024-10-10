import sys
sys.path.append("/Users/julietnwagwuume-ezeoke/_UILCode/gqe-phd/svg2plan/_scripts")

from fractions import Fraction
import json
from typing_extensions import Annotated
import typer
from dataclasses import dataclass
from typing import Literal, NamedTuple, Optional, Tuple
from rich.prompt import Prompt, PromptBase
from pint import UnitRegistry
from decimal import Decimal, localcontext
from helpers.shapely import ROUNDING_LIM
from pprint import pprint
from rich import print as rprint

## find a json file, or for now, create one. when complete, this will be passed from svg reader..

## speficy type, door or window.
## from there ask different questions.. so series of prompts..

## will have to enter in models, and materials as well..


def rounded_decimal_from_fraction(frac: Fraction):
    return round(frac.numerator / Decimal(frac.denominator), ROUNDING_LIM)


class FootInchesDimension(NamedTuple):
    feet: Fraction
    inches: tuple[Fraction, Fraction]

    def __repr__(self) -> str:
        return f"{self.feet}ft, {format(self.inches[0])} {format(self.inches[1])}in ({self.meters}m)"

    @property
    def meters(self):
        ureg = UnitRegistry()
        total_meters = 0
        fractional_inches = sum([Fraction(i) for i in self.inches])
        inches_as_meters = (fractional_inches * ureg.inches).to(ureg.meters)
        total_meters += inches_as_meters

        feet_as_meters = (Fraction(self.feet) * ureg.feet).to(ureg.meters)
        total_meters += feet_as_meters
        return rounded_decimal_from_fraction(total_meters.magnitude)  # type: ignore


@dataclass
class SubsurfaceBase:
    id: int
    width: FootInchesDimension
    height: FootInchesDimension

    def to_json(self):
        d = self.__dict__
        for k, v in d.items():
            if hasattr(v, "feet"):
                d[k] = str(v.meters)
        return d


@dataclass
class WindowType(SubsurfaceBase):
    head_height: FootInchesDimension
    model: str = "Andersen"
    type: Literal["Casement", "Fixed", "Casement+Fixed"] = "Casement"
    opening_hieght: FootInchesDimension = FootInchesDimension(
        Fraction(0), (Fraction(0), Fraction(0))
    )
    subsurface_type: str = "Window"


@dataclass
class DoorType(SubsurfaceBase):
    thickness: FootInchesDimension
    material: str  # TODO
    subsurface_type: str = "Door"


PATH = "test.json"

app = typer.Typer(no_args_is_help=True)


DimInput = Tuple[str, str, str]

def create_dimension(dim: DimInput):
    feet, *inches = dim
    fraction_inches = tuple([Fraction(i) for i in inches])
    assert len(fraction_inches) == 2

    return FootInchesDimension(feet=Fraction(feet), inches=fraction_inches)


@app.command()
def create_window(
    id: Annotated[int, typer.Argument(help="id")],
    width: Annotated[DimInput, typer.Option("--width", "-w")],
    height: Annotated[DimInput, typer.Option("--height", "-h")],
    head_height: Annotated[DimInput, typer.Option("--head-height", "-hh")],
):
    
    try:
        with open(PATH, "r") as file:
            windows: list[dict] = json.load(file)
    except:
        windows = []

    if windows:
        existing_ids = [i["id"] for i in windows]
        if id in existing_ids:
            rprint(f"ID {id} already exists. Incrementing to {id+1}")
            id+=1
            
    
    res = WindowType(
        id,
        create_dimension(width),
        create_dimension(height),
        create_dimension(head_height),
    )


    rprint(res)
    windows.append(res.to_json())


    with open(PATH, "w") as file:
        json.dump(windows, default=str, fp=file)


@app.callback()
def main(ctx: typer.Context):
    pass


if __name__ == "__main__":
    app()
