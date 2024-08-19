import os
from xml.dom import minidom
from dataclasses import dataclass

from shapely import LinearRing, Polygon


@dataclass
class SVGRect:
    x: str
    y: str
    width: str
    height: str
    id: str


class SVGReader:
    def __init__(self, svg_name) -> None:
        self.svg_path = os.path.join("../../svg_imports", svg_name)
        self.domains = {}

    def run(self):
        self.get_rectangles()
        self.convert_rectangles()

    def get_rectangles(self):
        doc = minidom.parse(self.svg_path)  # parseString also exists
        self.rectangles = [
            self.get_rectangle(path) for path in doc.getElementsByTagName("rect")
        ]
        doc.unlink()

    def get_rectangle(self, path):
        s = SVGRect(
            path.getAttribute("x"),
            path.getAttribute("y"),
            path.getAttribute("width"),
            path.getAttribute("height"),
            path.getAttribute("id"),
        )
        return s

    def convert_rectangles(self):
        for r in self.rectangles:
            self.domains[r.id] = self.get_shapely(r)

    def get_shapely(self, r: SVGRect):
        x0 = float(r.x) if r.x else 0
        y0 = float(r.y) if r.y else 0
        x1 = x0 + float(r.width)
        y1 = y0 - float(r.height)

        # ccw from bottom left
        coords = [(x0, y1), (x1, y1), (x1, y0), (x0, y0)]
        shape = Polygon(LinearRing(coords))

        return shape
