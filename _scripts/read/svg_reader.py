import os
from xml.dom import minidom

from read.interfaces import SVGRect
from read.conversion import ConversionPreparer

from helpers.shapely import domain_to_shape
from helpers.layout import PartialLayout
from constants import ROUNDING_LIM

from domains.domain import Domain
from domains.range import nonDecimalRange

from decimal import Decimal
from read.interfaces import SVGReference

PATH = "/Users/julietnwagwuume-ezeoke/_UILCode/gqe-phd/svg2plan/svg_imports"
svg_ref = SVGReference("bedroom_1", "width")

class SVGReader:
    def __init__(self, svg_name, px_len=Decimal("234"), real_len=Decimal("3.8862")) -> None:
        self.svg_path = os.path.join(PATH, svg_name)
        self.layout = PartialLayout({}, {})
        self.conversion = real_len / px_len

    def run(self):
        self.get_rectangles()
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


    def get_y_correction(self):
        ys = [r.y for r in self.rectangles]
        max_y = max(ys)
        max_ix = ys.index(max_y)
        # TODO doesnt actually work to zero out => need to get the correction after the fact!
        self.correction = max_y + self.rectangles[max_ix].height

    def convert_rectangles(self):
        for r in self.rectangles:
            self.create_domains(r)
            self.update_dimensions()
            self.layout.domains[r.id] = self.domain
            self.layout.shapes[r.id] = self.polygon

    def create_domains(self, r: SVGRect):
        x_left = r.x
        y_top = r.y * (-1)  # make +y in conventional +y direction

        x_right = x_left + float(r.width)
        y_bottom = y_top - float(r.height)

        y_bottom += self.correction
        y_top += self.correction

        self.temp_domain = Domain(
            name=r.id,
            x=nonDecimalRange(x_left, x_right).toRange(),
            y=nonDecimalRange(y_bottom, y_top).toRange(),
        )

    def update_dimensions(self):
        fx = lambda x: round(x * self.conversion, ROUNDING_LIM)
        self.domain = self.temp_domain.modify(fx)
        self.polygon = domain_to_shape(self.domain)
