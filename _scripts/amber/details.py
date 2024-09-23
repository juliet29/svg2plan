from adjacencies.connectivity import ConnectivityGenerator
from helpers.directions import Direction
from read.interfaces import SVGReference


# TODO -> move outside of scripts!!!

# windows
id3 = [
    ("m_bath", Direction.NORTH.name),
    ("m_bedroom", Direction.NORTH.name),
]
id11 = [
    ("kitchen", Direction.SOUTH.name),
]

# doors
id8 = [
    ("m_bath", "m_bedroom"),
    ("bath", "transit_space"),
]
id100 = [("kitchen", "dining")]


def update_surface_types(cg: ConnectivityGenerator):
    cg.update_id(id3, 3)
    cg.update_id(id11, 11)
    cg.update_id(id8, 8)
    cg.update_id(id100, 100)

    return cg


# reference length
REF_LENGTH_FT = 10
REF_LENGTH_IN = 6.75
# TODO put some checks on this!
svg_ref = SVGReference("bedroom_1", "width")
