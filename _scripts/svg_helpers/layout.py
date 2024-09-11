from dataclasses import dataclass
from typing import Dict, Optional
from svg_helpers.domains import Corners, DecimalCorners
from shapely import Polygon
from networkx import Graph


@dataclass
class Layout:
    shapes: Dict[str, Polygon]
    corners: Dict[str, Corners]
    graph: Graph


@dataclass
class PartialLayout:
    shapes: Dict[str, Polygon]
    corners: Dict[str, DecimalCorners]
