from dataclasses import dataclass
from typing import Dict, NamedTuple
from shapely import Polygon
from networkx import Graph, DiGraph
from domains.domain import Domain

DomainsDict = Dict[str, Domain]
OptionalDomainsDict = Dict[str, Domain|None]
ShapesDict = Dict[str, Polygon]

class DiGraphs(NamedTuple):
    Gx: DiGraph
    Gy: DiGraph

class Layout(NamedTuple):
    # shapes: ShapesDict
    domains: DomainsDict 
    graphs: DiGraphs




class PartialLayout(NamedTuple):
    shapes: ShapesDict
    domains: DomainsDict


def get_bounds_of_layout(coordinates: Dict[str, tuple]):
    x_values = [coord[0] for coord in coordinates.values()]
    y_values = [coord[1] for coord in coordinates.values()]

    x_min = min(x_values)
    x_max = max(x_values)
    y_min = min(y_values)
    y_max = max(y_values)

    return Domain.create_domain([x_min, x_max, y_min, y_max])
