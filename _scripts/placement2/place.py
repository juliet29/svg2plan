from itertools import product
import numpy as np
from copy import deepcopy
from icecream import ic
from domains.domain import Domain
from domains.range import Range
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


def create_new_domains(darr):
    return {v.name: v for v in darr.flatten() if v}

def create_new_shapes(darr):
    return {v.name: domain_to_shape(v) for v in darr.flatten() if v}


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


def calculate_size_of_x_overlap(a: Domain, b: Domain):
    u,v = sorted([a,b], key=lambda d: d.x.size)
    return u.x.line_string.intersection(v.x.line_string).length

def potential_x_domain(darr, curr_slice):
    row, col = curr_slice
    west_node = darr[row, col-1]
    curr_node = darr[curr_slice]
    x_adjusted_range = Range(west_node.x.max, west_node.x.max+curr_node.x.size)
    return Domain(x_adjusted_range, curr_node.y, name=curr_node.name)




def choose_north_node(darr, curr_slice):
    row, _ = curr_slice
    curr_node = potential_x_domain(darr, curr_slice)
    if curr_node.name == "linen":
        print(curr_node)
    northern_row = darr[row-1]

    max_overlap = (0, None)
    for node in northern_row:
        if not node:
            continue
        ov = calculate_size_of_x_overlap(curr_node, node)
        if ov > max_overlap[0]:
            max_overlap = (ov, node)

        if curr_node.name == "linen":
            print(max_overlap)
    assert max_overlap[1]

    

    
    return max_overlap[1]





def get_west_node(darr, curr_slice):
    def create_west_slice():
        return (curr_slice[0], col_cntr)

    col_cntr = curr_slice[1] - 1
    while not darr[create_west_slice()]:
        col_cntr -= 1
        if col_cntr < 0:
            raise Exception("No west node found")
    return darr[create_west_slice()]

def get_y_top(darr, curr_slice):
    row_ix, _ = curr_slice
    prev_row_ys = [i.y.min for i in darr[row_ix-1] if i]
    return min(prev_row_ys)

def handle_init_row(darr, s):
    node = darr[s]
    _, col = s
    if col == 0: 
        d = place_north_west(node)
    else:
        west_node = get_west_node(darr, s)
        d = place_east(node, west_node)
    return update_domains_arr(s, d, darr)

def handle_remaining_rows(darr, s):
    node = darr[s]
    
    _, col = s
    if col == 0: 
        north_node = get_north_node(darr,s) # TODO simplify
        d = place_south(node, north_node)
    else:
        north_node = choose_north_node(darr, s)
        west_node = get_west_node(darr, s)
        d = place_south_east(node, north_node, west_node)
    return update_domains_arr(s, d, darr)



def handle_node(darr, loc, visited_nodes):
    row_ix, _ = loc
    s = np.s_[loc]
    node = darr[s]
    if not node:
        return darr, visited_nodes
    
    if node.name in visited_nodes.keys():
        darr[s] = darr[visited_nodes[node.name]]
        return darr, visited_nodes
    else:
        visited_nodes[node.name] = s

    if row_ix == 0:
        return handle_init_row(darr, s), visited_nodes
    else:
        return handle_remaining_rows(darr, s), visited_nodes




def place_nodes(darr):
    indices = get_array_indices(darr)
    visited_nodes = {}
    for loc in indices:
            darr, visited_nodes = handle_node(darr, loc, visited_nodes)
    return darr





def create_placement_and_update_layout(layout):
    arr = create_arrangement(layout)
    darr = create_domains_arr(arr, layout.domains)
    darr1 = place_nodes(darr)

    return Layout(
        shapes=create_new_shapes(darr1),
        domains=create_new_domains(darr1),
        graph=layout.graph,
    )
