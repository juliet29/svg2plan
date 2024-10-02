from itertools import product
import numpy as np
from decimal import Decimal
from typing import Dict
from domains.domain import Domain
from copy import deepcopy
from icecream import ic


def calculate_domain_differences(domain: Domain):
    x_min, x_max, y_min, y_max = domain.get_values()
    dif_x = abs(x_max - x_min)
    dif_y = abs(y_max - y_min)
    return dif_x, dif_y

def create_new_domain(domain: Domain, new_x_left: Decimal, new_y_top: Decimal):
    dif_x, dif_y = calculate_domain_differences(domain)
    new_x_max = dif_x + new_x_left
    new_y_min = new_y_top - dif_y

    return Domain.create_domain(
            [new_x_left, new_x_max, new_y_min, new_y_top], domain.name
        )

def place_north_west(domain: Domain):
    new_x_left = Decimal(0)
    new_y_top = Decimal(0)
    return create_new_domain(domain, new_x_left, new_y_top)


def place_east(domain: Domain, west_domain: Domain):
    new_x_left = west_domain.x.max
    new_y_top = Decimal(0)
    return create_new_domain(domain, new_x_left, new_y_top)

def place_south(domain: Domain, north_domain: Domain):
    new_x_left = Decimal(0)
    new_y_top = north_domain.y.min
    return create_new_domain(domain, new_x_left, new_y_top)


def place_south_east(domain: Domain, north_domain: Domain, west_domain: Domain):
    new_x_left = west_domain.x.max
    new_y_top = north_domain.y.min
    return create_new_domain(domain, new_x_left, new_y_top)





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
        col_cntr-=1
        if col_cntr < 0:
            raise Exception("No north node found")
    return darr[create_north_slice()]

def get_west_node(darr, curr_slice):
    s = (curr_slice[0], curr_slice[1]-1)
    west_node = darr[s]
    assert west_node
    return west_node

def handle_init_col(darr, s, is_subsequent_row=False):
    node = darr[s]
    if not is_subsequent_row:
        print("first row, init col")
        d = place_north_west(darr[s])
        return update_domains_arr(s, d, darr)
    else:
        print("next row, init col")
        north_node = get_north_node(darr, s)
        d = place_south(node, north_node)
        return update_domains_arr(s, d, darr)
    
def handle_remaining_cols(darr, s, is_subsequent_row=False):
    node = darr[s]
    if not is_subsequent_row:
        print("first row, next col")
        west_node = get_west_node(darr, s)
        d = place_east(node, west_node)
        return update_domains_arr(s, d, darr)
    else:
        print("next row, next col")
        north_node = get_north_node(darr, s)
        west_node = get_west_node(darr, s)
        d = place_south_east(node, north_node, west_node)
        return update_domains_arr(s, d, darr)
    
def get_array_indices(arr):
    return list(product(*([i for i in range(sz)] for sz in arr.shape)))

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
    return {v.name:v for v in darr.flatten() if v} 