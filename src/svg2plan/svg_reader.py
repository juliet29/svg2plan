from pathlib import Path
from xml.dom import minidom
from typing import NamedTuple
from decimal import Decimal

from scipy import stats
import numpy as np

from helpers.utils import filter_none
from helpers.layout import PartialLayout, DomainsDict
from constants import ROUNDING_LIM, INIT_WORLD_LEN_M, INIT_PX_LEN

from domains.domain import Domain
from domains.range import nonDecimalRange


class SVGRect(NamedTuple):
    x: float
    y: float
    width: float
    height: float
    id: str


def filter_outlier_domains(domains: DomainsDict, threshold_z:int=2):
    domains_list = list(domains.values())
    areas = [i.area for i in domains_list]
    z = np.abs(stats.zscore(areas))
    outlier_indices = np.where(z > threshold_z)[0]
    valid_domains = [
        domains_list[ix]
        for ix, _ in enumerate(domains_list)
        if ix not in outlier_indices
    ]
    return {i.name: i for i in valid_domains}


class SVGReader:
    def __init__(
        self,
        svg_path: Path,
        px_len=Decimal(INIT_PX_LEN),
        real_len=Decimal(INIT_WORLD_LEN_M),
        filter_outliers=False
    ) -> None:
        assert svg_path.exists(), "Invalid SVG Path"
        self.svg_path = svg_path

        self.conversion_fx = lambda x: round(x * (real_len / px_len), ROUNDING_LIM)
        self.filter_outliers = filter_outliers



    def run(self):
        self.get_rectangles()
        self.get_y_correction()
        self.convert_rectangles()

    def get_rectangles(self):
        doc = minidom.parse(str(self.svg_path))
        self.rectangles = filter_none([
            self.parse_single_rectangle(path)
            for path in doc.getElementsByTagName("rect")
            if path.getAttribute("id")
        ])
        doc.unlink()

    def parse_single_rectangle(self, path):
        id=path.getAttribute("id")
        if "image" in id:
            return None
        return SVGRect(
            self.get_attr_as_float("x", path),
            self.get_attr_as_float("y", path),
            self.get_attr_as_float("width", path),
            self.get_attr_as_float("height", path),
            id=path.getAttribute("id"),
        )

    def get_attr_as_float(self, attr: str, path):
        value = path.getAttribute(attr)
        return float(value) if value else 0.0

    def convert_rectangles(self):
        self.init_domains = {}
        for r in self.rectangles:
            self.init_domains[r.id] = self.create_domain(r)

        if self.filter_outliers:
            self.domains = filter_outlier_domains(self.init_domains)
            diff = set(self.init_domains).difference(set(self.domains))
            if diff:
                print(f"Removed outlier domains: {diff}")
        else:
            self.domains = self.init_domains

    def get_y_correction(self):
        ys = [r.y for r in self.rectangles]
        max_y = max(ys)
        max_ix = ys.index(max_y)
        # TODO doesnt actually work to zero out
        self.correction = max_y + self.rectangles[max_ix].height

    def create_domain(self, r: SVGRect):
        x_left = r.x
        y_top = r.y * (-1)  # make +y in conventional +y direction

        x_right = x_left + float(r.width)
        y_bottom = y_top - float(r.height)

        y_bottom += self.correction
        y_top += self.correction

        return Domain(
            name=r.id,
            x=nonDecimalRange(x_left, x_right).toRange(),
            y=nonDecimalRange(y_bottom, y_top).toRange(),
        ).modify(self.conversion_fx)
