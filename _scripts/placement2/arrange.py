import numpy as np
from export.saver import read_pickle
from helpers.graph_helpers import sort_nodes_on_egde
from helpers.helpers import chain_flatten, filter_none
from helpers.layout import Layout
from copy import deepcopy
from icecream import ic
# layout: Layout = read_pickle("1001_amber_c_ag")

def initialize_arr(layout: Layout):
    sd = sort_nodes_on_egde(layout.graph, layout.domains)
    arr = np.full(shape=(len(sd["WEST"]), len(sd["NORTH"])), fill_value="", dtype=object)
    north_row = np.s_[0, :]
    west_col = np.s_[:, 0]

    # place north nodes and west nodes
    arr[north_row] = [i.name for i in sd["NORTH"]]
    arr[west_col] = [i.name for i in sd["WEST"]]
    return arr, sd, north_row, west_col

def get_unplaced(arr, domains):
    return set(domains.keys()).difference(set(np.unique(arr)))

def get_row(arr, ix):
    return list(arr[ix, :])

def get_node_with_north_nb_in_row(G, north_row, node):
    for i in G.nodes()[node]["data"]["NORTH"]:
        if i in north_row:
            return node

def get_north_and_east_nbs(G, north_row, node):
    return [(node,i) for i in north_row if i in G.nodes()[node]["data"]["EAST"]]

def get_possible_members_of_next_row(G, arr, ix):
    north_row = get_row(arr, ix)
    ic(north_row)
    next_row_members = filter_none([get_node_with_north_nb_in_row(G, north_row, node) for node in G.nodes])
    north_east_members = chain_flatten([get_north_and_east_nbs(G, north_row, node) for node in next_row_members])
    ic(north_east_members)


    return next_row_members



def find_east_nb(G, node, valid_nbs):
    east_nbs = G.nodes()[node]["data"]["EAST"]
    res = set(east_nbs).intersection(set(valid_nbs))
    if len(res) == 1:
        return list(res)[0]
    if len(res) == 0:
        return None
    if len(res) > 1:
        raise Exception("More than one east nb")
    

    

def create_next_row(G, arr, ix):
    valid_nodes = get_possible_members_of_next_row(G, arr, ix)
    found_nodes = [arr[ix+1, 0]]
    avail_nodes = list(set(valid_nodes).difference(set(found_nodes)))
    print(valid_nodes)

    max_iter = 10
    cnt = 0

    while avail_nodes:
        cnt+=1
        curr_node = found_nodes[-1]
        next_node = find_east_nb(G, curr_node, avail_nodes)
        if not next_node:
            return found_nodes
        else:
            found_nodes.append(next_node)
            curr_node = next_node
        if cnt > max_iter:
            raise Exception("Exceeded max iter")
        

        
def adjust_arr_for_row(arr, row):
    n_rows, n_cols = arr.shape
    if n_cols < len(row):
        diff = len(row) - n_cols
        temp = np.full(shape=(n_rows, diff), fill_value="", dtype=object)
        narr = np.hstack((arr, temp))
        return narr
    return deepcopy(arr)

def update_arr(arr, row, ix):
    narr = deepcopy(arr)
    narr[ix, 0:len(row)] = row
    return narr

def get_current_row(arr):
    for ix, i in enumerate(arr):
        if not i[1]: # i[0] are the west nodes
            return ix - 1
    raise Exception("Couldnt find current row")
    
def place_next_row(G, arr):
    ix = get_current_row(arr)
    row = create_next_row(G, arr, ix)
    narr = adjust_arr_for_row(arr, row)
    return update_arr(narr, row, ix+1)

def create_placement(layout):
    return [[]]