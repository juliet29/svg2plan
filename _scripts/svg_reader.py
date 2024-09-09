import os
from xml.dom import minidom
from dataclasses import dataclass

from shapely import LinearRing, Polygon

from svg_helpers.domains import Domain, Corners, DomainDict


@dataclass
class SVGRect:
    x: float
    y: float
    width: float
    height: float
    id: str




class SVGReader:
    def __init__(self, svg_name) -> None:
        self.svg_path = os.path.join("../svg_imports", svg_name)
        self.domains: DomainDict = {}

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
        x_left = r.x
        y_top = r.y * (-1) # make +y in conventional +y direction 


        x_right = x_left + float(r.width)
        y_bottom = y_top - float(r.height)

        y_bottom+=self.correction
        y_top+=self.correction

        # ccw from bottom left
        coords = [(x_left, y_bottom), (x_right, y_bottom), (x_right, y_top), (x_left, y_top)]

        polygon = Polygon(LinearRing(coords))
        corners = Corners(x_left, x_right, y_bottom, y_top)
        return Domain(polygon, corners)
    

    
    def get_attr_as_float(self, attr:str, path):
        value = path.getAttribute(attr)
        return float(value) if value else 0.0
 



