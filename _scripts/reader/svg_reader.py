import os
from xml.dom import minidom

from shapely import LinearRing, Polygon

from reader.interfaces import SVGRect
from reader.conversion import ConversionPreparer
from amber.details import svg_ref

from svg_helpers.domains import Domain, Corners, DomainDict, DecimalCorners
from svg_helpers.shapely import create_box_from_decimal_corners
from svg_helpers.layout import PartialLayout
from svg_helpers.constants import ROUNDING_LIM

from decimal import Decimal, getcontext

PATH = "/Users/julietnwagwuume-ezeoke/_UILCode/gqe-phd/svg2plan/svg_imports"

class SVGReader:
    def __init__(self, svg_name) -> None:
        self.svg_path = os.path.join(PATH, svg_name)
        self.domains = PartialLayout({}, {})

    def run(self):
        self.get_rectangles()
        self.prepare_to_update_dimensions()
        self.get_y_correction()
        self.convert_rectangles()

    def get_rectangles(self):
        doc = minidom.parse(self.svg_path)
        self.rectangles = [
            self.parse_single_rectangle(path)
            for path in doc.getElementsByTagName("rect")
        ]
        doc.unlink()

    def parse_single_rectangle(self, path):
        return SVGRect(
            self.get_attr_as_float("x", path),
            self.get_attr_as_float("y", path),
            self.get_attr_as_float("width", path),
            self.get_attr_as_float("height", path),
            path.getAttribute("id"),
        )

    def get_attr_as_float(self, attr: str, path):
        value = path.getAttribute(attr)
        return float(value) if value else 0.0

    def prepare_to_update_dimensions(self):
        self.du = ConversionPreparer(self.rectangles, svg_ref)

    def get_y_correction(self):
        ys = [r.y for r in self.rectangles]
        max_y = max(ys)
        max_ix = ys.index(max_y)
        # TODO doesnt actually work to zero out => need to get the correction after the fact!
        self.correction = max_y + self.rectangles[max_ix].height

    def convert_rectangles(self):
        for r in self.rectangles:
            self.get_corners(r)
            self.update_dimensions()
            self.domains.corners[r.id] = self.decimal_corners
            self.domains.shapes[r.id] = self.polyon

    def get_corners(self, r: SVGRect):
        x_left = r.x
        y_top = r.y * (-1)  # make +y in conventional +y direction

        x_right = x_left + float(r.width)
        y_bottom = y_top - float(r.height)

        y_bottom += self.correction
        y_top += self.correction

        self.corners = Corners(x_left, x_right, y_bottom, y_top)

    def update_dimensions(self):
        converted_vals = (
            round(Decimal(i * self.du.conversion), ROUNDING_LIM) for i in self.corners
        )
        self.decimal_corners = DecimalCorners(*converted_vals)
        self.polyon = create_box_from_decimal_corners(self.decimal_corners)
