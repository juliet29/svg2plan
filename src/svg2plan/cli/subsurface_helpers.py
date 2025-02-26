from typing import Literal, Tuple
from rich import print as rprint
from .interfaces import FootInchesDimension, SubSurfacesJSON
import json
from fractions import Fraction
from pathlib import Path

DimInput = Tuple[str, str, str]


def create_dimension(dim: DimInput):
    feet, *inches = dim
    fraction_inches = tuple([Fraction(i) for i in inches])
    assert len(fraction_inches) == 2

    return FootInchesDimension(feet=Fraction(feet), inches=fraction_inches)


def open_subsurface_json(PATH):
    try:
        with open(PATH, "r") as file:
            data: SubSurfacesJSON = json.load(file)
    except:
        rprint(f"{Path(PATH).name} is empty, initializing data.. ")
        data: SubSurfacesJSON = {"WINDOWS": [], "DOORS": []}
    return data


def validate_id(data, id):
    if data:
        existing_ids = [i["id"] for i in data]
        while id in existing_ids:
            rprint(f"ID {id} already exists. Incrementing to {id+1}")
            id += 1
    return id


valid_wtypes = ["Casement", "Fixed", "Casement+Fixed"]


def complete_wtype(incomplete: str):
    for name in valid_wtypes:
        if name.startswith(incomplete):
            yield (name)
        else:
            yield tuple(valid_wtypes)


def validate_wtype(wtype: str, opening_height: DimInput):
    assert wtype in valid_wtypes
    if wtype == "Casement+Fixed":
        assert opening_height != ("0", "0", "0")
