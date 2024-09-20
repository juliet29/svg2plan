from enum import Enum
from dataclasses import dataclass, field, fields
from svg_helpers.helpers import toJson


class Direction(Enum):
    NORTH = 0
    SOUTH = 1
    EAST = 2
    WEST = 3


def get_opposite_direction(direction: Direction):
    return DIRECTION_PAIRS[direction]

def get_axis(direction: Direction):
    return DIRECTION_AXIS[direction]


DIRECTION_PAIRS = {
    Direction.NORTH: Direction.SOUTH,
    Direction.SOUTH: Direction.NORTH,
    Direction.EAST: Direction.WEST,
    Direction.WEST: Direction.EAST,
}

DIRECTION_AXIS = {
    Direction.NORTH: "y",
    Direction.SOUTH: "y",
    Direction.EAST: "x",
    Direction.WEST: "x",
}

class GeneralDirection(Enum):
    NORTH_SOUTH = 0
    EAST_WEST = 1


@dataclass
class NeighborDirections:
    NORTH: list = field(default_factory=list)
    SOUTH: list = field(default_factory=list)
    EAST: list = field(default_factory=list)
    WEST: list = field(default_factory=list)

    def __getitem__(self, i):
        return getattr(self, i)

    def get_empty_directions(self):
        return [i for i in self.__annotations__ if len(self.__getitem__(i)) == 0]

    def to_json(self):
        return {
            "NORTH": self.NORTH,
            "SOUTH": self.SOUTH,
            "EAST": self.EAST,
            "WEST": self.WEST,
        }





@dataclass
class DirectedPairEW:
    EAST: str
    WEST: str

    def __repr__(self) -> str:
        l1 = f"DirectedPair(`{self.WEST} is WEST of {self.EAST}`)"
        return l1


@dataclass
class DirectedPairNS:
    NORTH: str
    SOUTH: str

    def __repr__(self) -> str:
        l1 = f"DirectedPair(`{self.NORTH} is NORTH of {self.SOUTH}`)"
        return l1


def make_directed_pairEW(G, u, v):
    u_data = G.nodes(data=True)[u]
    if v in u_data["data"].EAST:
        d = DirectedPairEW(EAST=v, WEST=u)
    elif v in u_data["data"].WEST:
        d = DirectedPairEW(EAST=u, WEST=v)
    else:
        print("No EW relation")
        return

    return d


def make_directed_pairNS(G, u, v):
    u_data = G.nodes(data=True)[u]
    if v in u_data["data"].NORTH:
        d = DirectedPairNS(NORTH=v, SOUTH=u)
    elif v in u_data["data"].SOUTH:
        d = DirectedPairNS(NORTH=u, SOUTH=v)
    else:
        print("No NS relation")
        return

    return d


def make_directed_pair(G, u, v):
    u_data = G.nodes(data=True)[u]
    possible_pairs = []
    if v in u_data["data"].EAST:
        possible_pairs.append(DirectedPairEW(EAST=v, WEST=u))
    if v in u_data["data"].WEST:
        possible_pairs.append(DirectedPairEW(EAST=u, WEST=v))
    if v in u_data["data"].NORTH:
        possible_pairs.append(DirectedPairNS(NORTH=v, SOUTH=u))
    if v in u_data["data"].SOUTH:
        possible_pairs.append(DirectedPairNS(NORTH=u, SOUTH=v))

    return possible_pairs
