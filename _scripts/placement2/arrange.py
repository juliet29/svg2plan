import numpy as np
from helpers.graph_helpers import sort_nodes_on_egde
from helpers.helpers import chain_flatten, filter_none
from helpers.layout import Layout
from copy import deepcopy
from icecream import ic
from svg_logger.settings import svlogger


def create_string_2d_array(shape: tuple[int, int]):
    return np.full(shape=shape, fill_value="", dtype=object)


def get_row(arr, ix):
    return list(arr[ix, :])


def get_unplaced(arr, domains):
    return set(domains.keys()).difference(set(np.unique(arr)))


def remove_existing_node_from_list(arr, lst):
    return list(set(lst).difference(set(arr.flatten())))


def initialize_arr(layout: Layout):
    sorted_domains = sort_nodes_on_egde(layout.graph, layout.domains)
    arr = create_string_2d_array(
        shape=(len(sorted_domains["WEST"]), len(sorted_domains["NORTH"]))
    )

    # place north nodes and west nodes
    arr[0, :] = [i.name for i in sorted_domains["NORTH"]]
    arr[:, 0] = [i.name for i in sorted_domains["WEST"]]
    return arr


def get_node_with_north_nb_in_row(G, north_row, node):
    for i in G.nodes()[node]["data"]["NORTH"]:
        if i in north_row:
            return node


def get_north_and_east_nbs(G, north_row, node):
    return [i for i in north_row if i in G.nodes()[node]["data"]["EAST"]]


def get_possible_members_of_next_row(G, arr, ix):
    north_row = get_row(arr, ix)
    next_row = filter_none(
        [get_node_with_north_nb_in_row(G, north_row, node) for node in G.nodes]
    )
    north_east = chain_flatten(
        [get_north_and_east_nbs(G, north_row, node) for node in next_row]
    )
    if north_east:
        svlogger.debug(f"NORTH EAST node added when processing {ix}: {north_east}")

    return list(set(next_row).union(set(north_east)))


def find_east_nb(G, arr, node, possible_nbs):
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
            raise Exception("More than one east nb")


def create_next_row(G, arr, ix):
    possible_nodes = get_possible_members_of_next_row(G, arr, ix)
    found_nodes = [arr[ix + 1, 0]]  # TODO make fx => western node of row
    avail_nodes = list(set(possible_nodes).difference(set(found_nodes)))
    if not avail_nodes:
        return found_nodes

    max_iter = 10
    cnt = 0

    while avail_nodes:
        curr_node = found_nodes[-1]
        next_node = find_east_nb(G, arr, curr_node, avail_nodes)

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
        narr = np.hstack((arr, temp))
        return narr
    return deepcopy(arr)


def update_arr(arr, row, ix):
    narr = deepcopy(arr)
    narr[ix, 0 : len(row)] = row
    return narr


def get_current_row(arr):
    for ix, i in enumerate(arr):
        if not i[1]:  # i[0] are the west nodes but
            return ix - 1
        # TODO not  a good approach bc could have just one node in a row and thats not a problem..
    raise Exception("Couldnt find current row")


def place_next_row(G, arr):
    ix = get_current_row(arr)
    row = create_next_row(G, arr, ix)
    narr = adjust_arr_for_row(arr, row)
    return update_arr(narr, row, ix + 1)


def create_arrangement(layout):
    arr = initialize_arr(layout)
    unplaced = get_unplaced(arr, layout.domains)
    max_iter = 10
    cnt = 0

    while unplaced:
        arr = place_next_row(layout.graph, arr)
        unplaced = get_unplaced(arr, layout.domains)

        cnt += 1
        if cnt > max_iter:
            raise Exception("Exceeded max iter")

    return arr
