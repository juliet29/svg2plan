from dataclasses import dataclass
from typing import Dict, Optional
from shapely import Polygon
from networkx import Graph
from new_corners.domain import Domain


@dataclass
class Layout:
    shapes: Dict[str, Polygon]
    domains: Dict[str, Domain]
    graph: Graph


@dataclass
class PartialLayout:
    shapes: Dict[str, Polygon]
    domains: Dict[str, Domain]


def get_bounds_of_layout(coordinates: Dict[str, tuple]):
        x_values = [coord[0] for coord in coordinates.values()]
        y_values = [coord[1] for coord in coordinates.values()]


        x_min = min(x_values)
        x_max = max(x_values)
        y_min = min(y_values)
        y_max = max(y_values)

        return Domain.create_domain([x_min, x_max, y_min, y_max])