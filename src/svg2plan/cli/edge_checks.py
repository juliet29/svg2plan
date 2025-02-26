from .interfaces import EdgeDetails, SubsurfaceType
from .helpers import error_print


class InvalidAssignmentError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


def is_valid_id(subsurfaces, id):
    valid_ids = [item["id"] for item in subsurfaces]
    if not id in valid_ids:
        error_print(f"passed {id} is not in subsurface ids: {valid_ids}")


def are_all_same_type(edge_types, relevant_edges):
    if not len(set(edge_types)) == 1:
        error_print(
            f"Should only have one kind of edge, but instead have {relevant_edges}"
        )


def are_matching_subsurface_type(
    subsurface_type, edge_types, relevant_edges: list[EdgeDetails]
):
    m = f"Should only have internal edges for subsurface type {subsurface_type}. If meant to add windows, add '--window' or '-w' to end of call"

    def find_wrong_edges(is_external):
        wrong_edges = []
        for i in relevant_edges:
            if i.external != is_external:
                wrong_edges.append(i)
        return " .Wrong Eges: " + " ".join([str(i.ix) for i in wrong_edges])

    if subsurface_type == SubsurfaceType.DOORS:
        if not all(edge_types) == False:
            error_print(m + find_wrong_edges(False))
    else:
        if not all(edge_types) == True:
            error_print(m + find_wrong_edges(True))


def are_connectivity_edges(edge_details, n_edges, relevant_edges):
    connectivity_edges = set([item.ix for item in edge_details if item.connectivity])
    if not set(n_edges) <= connectivity_edges:
        error_print(f"Edges are not connectivity edges: {relevant_edges} ")


def is_valid_assignment(id, subsurface_type, subsurfaces, edge_details, edge_ids):
    # TODO when creating edges, said that external must be window, but always true..
    relevant_edges = [i for i in edge_details if i.ix in edge_ids]
    edge_types = [i.external for i in relevant_edges]
    is_valid_id(subsurfaces, id)
    are_all_same_type(edge_types, relevant_edges)
    are_matching_subsurface_type(subsurface_type, edge_types, relevant_edges)
    are_connectivity_edges(edge_details, edge_ids, relevant_edges)
