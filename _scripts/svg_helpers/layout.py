from dataclasses import dataclass
from typing import Dict, Optional
from svg_helpers.domains import Corners, Domain
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



