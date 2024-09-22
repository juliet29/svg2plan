from pint import UnitRegistry, Quantity
from svg_helpers.domains import Corners
from amber.details import REF_LENGTH_IN, REF_LENGTH_FT
from reader.interfaces import SVGRect
from reader.interfaces import SVGReference


class ConversionPreparer:
    def __init__(
        self,
        rectangles: list[SVGRect],
        reference: SVGReference,
        ref_length: Quantity | None = None,
    ) -> None:
        self.rectangles = rectangles
        self.reference = reference
        self.ref_length = ref_length

        self.ureg = UnitRegistry()

        self.run()

    def run(self):
        self.get_svg_reference()
        self.create_conversion()

    def get_svg_reference(self):
        try:
            [room] = [i for i in self.rectangles if i.id == self.reference.id]
            self.svg_length = float(room.__getattribute__(self.reference.dimension))
        except ValueError:
            print("No reference for svg to meters conversion!! ")
            self.svg_length = 234


    def create_conversion(self):
        if not self.ref_length:
            self.ref_length = (
                Quantity(
                    REF_LENGTH_FT * self.ureg.feet + REF_LENGTH_IN * self.ureg.inches
                )
            ).to(self.ureg.meter)

        assert self.ref_length.units == self.ureg.meter

        self.conversion_w_units = self.ref_length / self.svg_length
        self.conversion: float = self.conversion_w_units.magnitude
