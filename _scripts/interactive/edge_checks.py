from interactive.interfaces import SubsurfaceType
from interactive.helpers import error_print

class InvalidAssignmentError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

def is_valid_id(subsurfaces, id):
    valid_ids = [item["id"] for item in subsurfaces]
    if not id in valid_ids:
        error_print(f"passed {id} is not in subsurface ids: {valid_ids}")


def are_all_same_type(edge_types, relevant_edges):
    if not len(set(edge_types)) == 1:
        error_print(f"Should only have one kind of edge, but instead have {relevant_edges}")
    

def are_matching_subsurface_type(subsurface_type, edge_types):
    m = f"Should only have internal edges for subsurface type {subsurface_type}. If meant to add windows, add '--window' or '-w' to end of call" 
    if subsurface_type == SubsurfaceType.DOORS:
        if not all(edge_types) == False:
            error_print(m)
    else:
        if not all(edge_types) == True:
            error_print(m)

def are_connectivity_edges(edge_details, n_edges, relevant_edges):
    connectivity_edges = set([item.ix for item in edge_details if item.connectivity])
    if not set(n_edges) <= connectivity_edges:
        error_print(f"Edges are not connectivity edges: {relevant_edges} ")
   
def is_valid_assignment(id, subsurface_type, subsurfaces, relevant_edges, edge_details, n_edges):
    edge_types = [i.external for i in relevant_edges]
    is_valid_id(subsurfaces, id)
    are_all_same_type(edge_types, relevant_edges)
    are_matching_subsurface_type(subsurface_type, edge_types)
    are_connectivity_edges(edge_details, n_edges, relevant_edges)