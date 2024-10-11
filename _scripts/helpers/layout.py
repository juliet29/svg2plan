from dataclasses import dataclass
from typing import Dict, NamedTuple
from shapely import Polygon
from networkx import Graph, DiGraph
from domains.domain import Domain

DomainsDict = Dict[str, Domain]
OptionalDomainsDict = Dict[str, Domain | None]
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



