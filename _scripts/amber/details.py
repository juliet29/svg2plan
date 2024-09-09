from adjacencies.connectivity import ConnectivityGenerator
from svg_helpers.directions import Direction

# windows
id3 = [('m_bath', Direction.NORTH.name),  
       ('m_bedroom', Direction.NORTH.name),]
id11 = [('kitchen', Direction.SOUTH.name),  ]

# doors
id8 = [('m_bath', "m_bedroom"),  
       ('bath', "transit_space"),]
id100 = [("kitchen", "dining")]


def update_surface_types(cg: ConnectivityGenerator):
    cg.update_id(id3, 3)
    cg.update_id(id11, 11)
    cg.update_id(id8, 8)
    cg.update_id(id100, 100)

    return cg

