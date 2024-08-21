from enum import Enum
from dataclasses import dataclass,field

class Direction(Enum):
    NORTH = 0
    SOUTH = 1
    EAST = 2
    WEST = 3

@dataclass
class NeighborDirections:
    NORTH: list = field(default_factory=list)
    SOUTH: list = field(default_factory=list)
    EAST: list = field(default_factory=list)
    WEST: list = field(default_factory=list)

    def __getitem__(self, i):
        return getattr(self, i)
    

pairs  = {
    Direction.NORTH: Direction.SOUTH,
    Direction.SOUTH: Direction.NORTH,
    Direction.EAST: Direction.WEST,
    Direction.WEST: Direction.EAST,
}

