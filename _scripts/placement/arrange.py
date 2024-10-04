import numpy as np
import networkx as nx
from typing import Dict, Iterable, NamedTuple
from domains.domain import Domain
from helpers.graph_helpers import sort_nodes_on_egde
from helpers.helpers import chain_flatten, filter_none
from helpers.layout import Layout
from copy import deepcopy
from icecream import ic
from svg_logger.settings import svlogger

class GraphDomains(NamedTuple):
    G: nx.Graph
    domains: Dict[str, Domain]


def create_string_2d_array(shape: tuple[int, int]):
    return np.full(shape=shape, fill_value="", dtype=object)


def get_row(arr, ix):
    return list(arr[ix, :])


def get_unplaced(arr, domains):
    return set(domains.keys()).difference(set(np.unique(arr)))


def remove_existing_node_from_list(arr, lst):
    return list(set(lst).difference(set(arr.flatten())))

def get_higher_nb(graph_domains:GraphDomains, nbs: Iterable[str]):
    return sorted(nbs, key=lambda n: graph_domains.domains[n].y.max, reverse=True)[0]


def initialize_arr(layout: Layout):
    sorted_domains = sort_nodes_on_egde(layout.graph, layout.domains)
    arr = create_string_2d_array(
        shape=(len(sorted_domains["WEST"]), len(sorted_domains["NORTH"]))
    )

    # place north nodes and west nodes
    arr[0, :] = [i.name for i in sorted_domains["NORTH"]]
    arr[:, 0] = [i.name for i in sorted_domains["WEST"]]
    return arr


def get_node_south_of_north_row(G, north_row, node):
    for i in G.nodes()[node]["data"]["NORTH"]:
        if i in north_row:
            return node


def get_north_and_east_nbs(G, north_row, node):
    return [i for i in north_row if i in G.nodes()[node]["data"]["EAST"]]


def get_possible_members_of_next_row(G, arr, ix):
    north_row = get_row(arr, ix)
    next_row = filter_none(
        [get_node_south_of_north_row(G, north_row, node) for node in G.nodes]
    )
    north_east = chain_flatten(
        [get_north_and_east_nbs(G, north_row, node) for node in next_row]
    )
    if north_east:
        svlogger.debug(f"nodes with north AND east relationships for members of row {ix+1}: {north_east}")

    return list(set(next_row).union(set(north_east)))


def find_east_nb(graph_domains:GraphDomains, arr, node, possible_nbs):
    G = graph_domains.G
    east_nbs = G.nodes()[node]["data"]["EAST"]
    res = set(east_nbs).intersection(set(possible_nbs))
    if len(res) == 1:
        return list(res)[0]
    if len(res) == 0:
        return None
    if len(res) > 1:
        r = remove_existing_node_from_list(arr, res)
        if len(r) == 1:
            return list(r)[0]
        else:
            return get_higher_nb(graph_domains, res)


def create_next_row(graph_domains:GraphDomains, arr, ix):
    G = graph_domains.G
    possible_nodes = get_possible_members_of_next_row(G, arr, ix)
    found_nodes = [arr[ix + 1, 0]]  # TODO make fx => westmost node
    avail_nodes = list(set(possible_nodes).difference(set(found_nodes)))
    if not avail_nodes:
        return found_nodes

    max_iter = 10
    cnt = 0

    while avail_nodes:
        curr_node = found_nodes[-1]
        next_node = find_east_nb(graph_domains, arr, curr_node, avail_nodes)

        if not next_node:
            return found_nodes
        else:
            found_nodes.append(next_node)
            curr_node = next_node

        cnt += 1
        if cnt > max_iter:
            raise Exception("Exceeded max iter")


def adjust_arr_for_row(arr, row):
    n_rows, n_cols = arr.shape
    if n_cols < len(row):
        diff = len(row) - n_cols
        temp = create_string_2d_array(shape=(n_rows, diff))
        return np.hstack((arr, temp))
    return deepcopy(arr)


def update_arr(arr, row, ix):
    narr = deepcopy(arr)
    narr[ix, 0 : len(row)] = row
    return narr


def get_current_row(arr):
    for ix, row in enumerate(arr):
        if not row[1]: 
            return ix - 1
        # TODO not  a good approach bc could have just one node in a row and thats not a problem..

    # OR all rows are filled and we are out of rows.. 
    raise Exception("Couldnt find current row")

def extend_arr(arr):
    temp = create_string_2d_array(shape=(1, arr.shape[1]))
    temp[0, 0] = arr[-1,0]
    return np.vstack((arr, temp))



def place_next_row(graph_domains:GraphDomains, arr):
    G = graph_domains
    try:
        ix = get_current_row(arr)
    except:
        arr = extend_arr(arr)
        ix = get_current_row(arr)
    row = create_next_row(G, arr, ix)
    narr = adjust_arr_for_row(arr, row)
    return update_arr(narr, row, ix + 1)

def is_sharing_north_nb(G, curr_node, west_node):
   curr =  set(G.nodes[curr_node]["data"]["NORTH"])
   west = set(G.nodes[west_node]["data"]["NORTH"])
   return bool(curr.intersection(west))

def is_west_nb(G, curr_node, west_node):
    return west_node in G.nodes[curr_node]["data"]["WEST"]

def handle_unplaced(graph_domains:GraphDomains, arr):
    unplaced = list(get_unplaced(arr, graph_domains.domains))
    if not unplaced:
        return arr
    
    west_node = arr[-1,0]
    G, domains = graph_domains 

    def is_lingering(curr_node):
        return not is_sharing_north_nb(G, curr_node, west_node) and not is_west_nb(G, curr_node, west_node)
    
    
    lingering = [i for i in unplaced if is_lingering(i)]
    assert len(lingering) == len(unplaced), "Not all unplaced nodes are lingering.. "
    if len(lingering) > (arr.shape[1] - 1):
        raise Exception("lingering nodes > than available space.. ")
    
    # TODO think about south relationships.. 
    sorted_lingering = sorted(lingering, key=lambda n: domains[n].x.min)
    row = deepcopy(arr[-1])
    row[-(len(lingering)):] = sorted_lingering
    indices = [ix for ix, item in enumerate(row) if not item]
    row[indices] = arr[-2, indices]
    new_arr = deepcopy(arr)
    new_arr[-1] = row

    return new_arr
    


def create_arrangement(layout):
    graph_domains = GraphDomains(layout.graph, layout.domains)
    arr = initialize_arr(layout)
    unplaced = get_unplaced(arr, layout.domains)
    max_iter = 10
    cnt = 0

    while unplaced:
        arr = place_next_row(graph_domains, arr)
        unplaced = get_unplaced(arr, layout.domains)

        cnt += 1 # TODO make this instead dependent on the array not changing.. 
        if cnt > max_iter:
            print("iterations exceeded, handling unplaced.. ")
            arr = handle_unplaced(graph_domains, arr)
            return arr
    

    return arr
