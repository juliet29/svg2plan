from itertools import product
import numpy as np
from copy import deepcopy
from icecream import ic
from helpers.shapely import domain_to_shape
from placement2.calculate import (
    place_east,
    place_north_west,
    place_south,
    place_south_east,
)
from placement2.arrange import create_arrangement
from helpers.layout import Layout


def get_array_indices(arr):
    return list(product(*([i for i in range(sz)] for sz in arr.shape)))


def remove_repeat_nodes(arr):
    unique, counts = np.unique(arr, return_counts=True)
    for item, count in zip(unique, counts):
        if item and count > 1:
            xs, ys = np.where(arr == item)
            locs = [np.s_[x, y] for x, y in zip(xs, ys)]
            for loc in locs[1:]:
                arr[loc] = ""
    return arr


def create_domains_arr(arr, domains):
    def get_domains(i):
        if i:
            return domains[i]
    return np.vectorize(get_domains)(arr)


def update_domains_arr(s, domain, domains_arr):
    new_darr = deepcopy(domains_arr)
    new_darr[s] = domain
    return new_darr


def get_north_node(darr, curr_slice):
    def create_north_slice():
        return (curr_slice[0] - 1, col_cntr)

    col_cntr = curr_slice[1]
    while not darr[create_north_slice()]:
        col_cntr -= 1
        if col_cntr < 0:
            raise Exception("No north node found")
    return darr[create_north_slice()]


def get_west_node(darr, curr_slice):
    def create_west_slice():
        return (curr_slice[0], col_cntr)

    col_cntr = curr_slice[1] - 1
    while not darr[create_west_slice()]:
        col_cntr -= 1
        if col_cntr < 0:
            raise Exception("No west node found")
    return darr[create_west_slice()]


def handle_init_col(darr, s, is_subsequent_row=False):
    node = darr[s]
    if not is_subsequent_row:
        d = place_north_west(node)
    else:
        north_node = get_north_node(darr, s)
        d = place_south(node, north_node)
    return update_domains_arr(s, d, darr)


def handle_remaining_cols(darr, s, is_subsequent_row=False):
    node = darr[s]
    if not is_subsequent_row:
        west_node = get_west_node(darr, s)
        d = place_east(node, west_node)
    else:
        north_node = get_north_node(darr, s)
        west_node = get_west_node(darr, s)
        d = place_south_east(node, north_node, west_node)
    return update_domains_arr(s, d, darr)


def handle_node(darr, loc):
    row_ix, ix = loc
    s = np.s_[row_ix, ix]
    if not darr[s]:
        return darr
    if ix == 0:
        return handle_init_col(darr, s, bool(row_ix))
    else:
        return handle_remaining_cols(darr, s, bool(row_ix))


def place_nodes(darr):
    indices = get_array_indices(darr)
    for loc in indices:
        darr = handle_node(darr, loc)
    return darr


def create_new_domains(darr):
    return {v.name: v for v in darr.flatten() if v}

def create_new_shapes(darr):
    return {v.name: domain_to_shape(v) for v in darr.flatten() if v}


def create_placement_and_update_layout(layout):
    arr = create_arrangement(layout)
    arr = remove_repeat_nodes(arr)
    darr = create_domains_arr(arr, layout.domains)
    darr1 = place_nodes(darr)

    return Layout(
        shapes=create_new_shapes(darr1),
        domains=create_new_domains(darr1),
        graph=layout.graph,
    )
