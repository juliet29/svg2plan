import os
from xml.dom import minidom
from dataclasses import dataclass

from shapely import LinearRing, Polygon


@dataclass
class SVGRect:
    x: float
    y: float
    width: float
    height: float
    id: str


class SVGReader:
    def __init__(self, svg_name) -> None:
        self.svg_path = os.path.join("../../svg_imports", svg_name)
        self.domains = {}

    def run(self):
        self.get_rectangles()
        self.get_y_correction()
        self.convert_rectangles()

    def get_rectangles(self):
        doc = minidom.parse(self.svg_path)
        self.rectangles = [
            self.get_rectangle(path) for path in doc.getElementsByTagName("rect")
        ]
        doc.unlink()

    def convert_rectangles(self):
        for r in self.rectangles:
            self.domains[r.id] = self.get_shapely(r)
        # slide each domain up so that there are no negative y values 
        
        



    def get_rectangle(self, path):
        return SVGRect(
            self.get_attr_as_float("x", path),
            self.get_attr_as_float("y", path),
            self.get_attr_as_float("width", path),
            self.get_attr_as_float("height", path),
            path.getAttribute("id"),
        )
    
    def get_y_correction(self):
        ys = [r.y for r in self.rectangles]
        max_y = max(ys)
        max_ix = ys.index(max_y)
        # TODO doesnt actually work to zero out => need to get the correction after the fact! 
        self.correction = max_y + self.rectangles[max_ix].height 

    

    def get_shapely(self, r: SVGRect):
        x0 = r.x
        y0 = r.y * - 1 #y + height


        x1 = x0 + float(r.width)
        y1 = y0 - float(r.height)

        # ccw from bottom left
        coords = [(x0, y1), (x1, y1), (x1, y0), (x0, y0)]
        coords = [(c[0], c[1]+self.correction) for c in coords]
        return Polygon(LinearRing(coords))
    

    
    def get_attr_as_float(self, attr:str, path):
        value = path.getAttribute(attr)
        return float(value) if value else 0.0
 



