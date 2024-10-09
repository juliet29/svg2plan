from fractions import Fraction
from typing_extensions import Annotated
import typer
from dataclasses import dataclass
from typing import Literal, NamedTuple, Optional, Tuple
from rich.prompt import Prompt, PromptBase

## find a json file, or for now, create one. when complete, this will be passed from svg reader..

## speficy type, door or window.
## from there ask different questions.. so series of prompts..

## will have to enter in models, and materials as well..


class FootInchesDimension(NamedTuple):
    foot: Fraction
    inches: tuple[Fraction, Fraction]

    def __repr__(self) -> str:
        return f"{self.foot} ft, {format(self.inches[0])}  {format(self.inches[1])} in"
    def as_meters(self):
        pass

@dataclass
class SubsurfaceBase():
    id: int
    width: FootInchesDimension
    height: FootInchesDimension

@dataclass
class WindowType(SubsurfaceBase):
    head_height: FootInchesDimension
    model: str  = "Andersen"
    type: Literal["Casement", "Fixed", "Casement+Fixed"] = "Casement"
    opening_hieght: FootInchesDimension = FootInchesDimension(
        Fraction(0), (Fraction(0), Fraction(0))
    )

@dataclass
class DoorType(SubsurfaceBase):
    thickness: FootInchesDimension
    material: str  # TODO


file = "test.json"

app = typer.Typer(no_args_is_help=True)

window_types = {}
door_types = {}


def create_dimension(dim: list[str]):
    assert len(dim) == 3
    feet, *inches = dim
    fraction_inches = tuple([Fraction(i) for i in inches])
    assert len(fraction_inches) == 2

    res = FootInchesDimension(foot=Fraction(feet), inches=fraction_inches)
    print(res)
    return res


def prompt_for_dim(dim_type: str):
    # comma seperated 2,3,4/5
    res = Prompt.ask(f"{dim_type.title()}")
    return create_dimension(res.split(","))


@app.command()
def create_window(
    id: Annotated[int, typer.Option(help="id")],
    types=window_types
):
    ## print existing ids, and modify if id is same as existing
    print(f"Creating window with id: {id}")
    
    width = prompt_for_dim("width")
    height = prompt_for_dim("height")
    head_height = prompt_for_dim("head_height")

    res = WindowType(id, width, height, head_height)
    window_types[id] = res
    print(window_types)
    return 


@app.callback()
def main(ctx: typer.Context):
    pass


if __name__ == "__main__":
    app()
