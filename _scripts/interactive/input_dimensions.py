from datetime import datetime
from typing import Tuple, Optional, List
from fractions import Fraction
from typing_extensions import Annotated
import typer
from pint import UnitRegistry
from decimal import Decimal, localcontext
# from svg_logger.settings import svlogger


def decimal_from_fraction(frac: Fraction):
    with localcontext() as ctx:
        ctx.prec = 4
        return frac.numerator / Decimal(frac.denominator)


def convert_feet_and_inches_to_meters(
    feet: Annotated[int, typer.Option("-f", help="feet")] = 0,
    inches: Annotated[Optional[Tuple[str, str]], typer.Option("-i", help="inches")] = ("0","0")
):
    total_meters = 0
    ureg = UnitRegistry()
    if inches:
        fractional_inches = sum([Fraction(i) for i in inches])
        inches_as_meters = (fractional_inches * ureg.inches).to(ureg.meters)
        print(f"{(fractional_inches * ureg.inches)}")
        total_meters += inches_as_meters
    if feet:
        feet_as_meters = (Fraction(feet) * ureg.feet).to(ureg.meters)
        print(f"{(feet * ureg.feet)}")
        total_meters += feet_as_meters

    print(decimal_from_fraction(total_meters.magnitude), "meters") # type: ignore
    return decimal_from_fraction(total_meters.magnitude) # type: ignore




if __name__ == "__main__":
    typer.run(convert_feet_and_inches_to_meters)
