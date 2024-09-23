from collections import namedtuple
from dataclasses import dataclass

SVGReference = namedtuple("SVGReference", ["id", "dimension"])


@dataclass
class SVGRect:
    x: float
    y: float
    width: float
    height: float
    id: str
