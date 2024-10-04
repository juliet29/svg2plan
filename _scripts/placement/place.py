from typing import Dict
from xml import dom
import networkx as nx
from itertools import combinations, product
import numpy as np
from copy import deepcopy
from icecream import ic
from shapely import Polygon
from domains.domain import Domain
from domains.range import Range
from helpers.shapely import domain_to_shape
from placement.calculate import (
    place_east,
    place_north_west,
    place_south,
    place_south_east,
)
from placement.arrange import create_arrangement
from helpers.layout import Layout


def create_domains_arr(arr:np.ndarray, domains: Dict[str, Domain]) -> np.ndarray:
    def get_domains(i):
        if i:
            return domains[i]
    return np.vectorize(get_domains)(arr)


def update_domains_arr(s, domain, domains_arr):
    new_darr = deepcopy(domains_arr)
    new_darr[s] = domain
    return new_darr


def calculate_size_of_x_overlap(a: Domain, b: Domain):
    u,v = sorted([a,b], key=lambda d: d.x.size)
    return u.x.line_string_x.intersection(v.x.line_string_x).length

def potential_x_domain(darr, curr_slice):
    row, col = curr_slice
    west_node = darr[row, col-1]
    curr_node = darr[curr_slice]
    x_adjusted_range = Range(west_node.x.max, west_node.x.max + curr_node.x.size)
    return Domain(x_adjusted_range, curr_node.y, name=curr_node.name)



def choose_north_node(darr, curr_slice, new_x_domain):
    row, _ = curr_slice
    northern_row = darr[row-1]

    max_overlap = (0, None)
    for node in northern_row:
        if not node:
            continue
        ov = calculate_size_of_x_overlap(new_x_domain, node)
        if ov > max_overlap[0]:
            max_overlap = (ov, node)

    assert max_overlap[1]
    return max_overlap[1]


def get_north_node(darr, curr_slice):
    row, col = curr_slice
    return darr[row-1, col]


def get_west_node(darr, curr_slice):
    row, col = curr_slice
    return darr[row, col-1]

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
        north_node = get_north_node(darr,s) 
        d = place_south(node, north_node)
    else:
        new_x_domain = potential_x_domain(darr, s)
        north_node = choose_north_node(darr, s, new_x_domain)
        d = place_south_east(node, north_node, new_x_domain)
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


def get_array_indices(arr):
    return list(product(*([i for i in range(sz)] for sz in arr.shape)))


def place_nodes(darr):
    indices = get_array_indices(darr)
    visited_nodes = {}
    for loc in indices:
            darr, visited_nodes = handle_node(darr, loc, visited_nodes)
    return darr




def create_new_domains(darr) -> Dict[str, Domain]:
    return {v.name: v for v in darr.flatten() if v}

def create_new_shapes(darr) -> Dict[str, Polygon]:
    return {v.name: domain_to_shape(v) for v in darr.flatten() if v}

def update_graph(shapes, graph):
    # NEEDS UPDATED LAYOUT!
    def get_shapes(pair):
        u, v = pair
        return shapes[u], shapes[v]
    
    def check_adjacency_simple(a:Polygon, b:Polygon):
        return a.intersects(b)
    
    def create_set(edges):
        return set([tuple(sorted(i)) for i in edges])


    G = deepcopy(graph)
    pairs = list(combinations(shapes.keys(), 2))
    new_edges = [pair for pair in pairs if check_adjacency_simple(*get_shapes(pair))]
    a, b = create_set(new_edges), create_set(G.edges)
    G.add_edges_from(a.difference(b))

    return G
    



def create_placement_and_update_layout(layout:Layout):
    arr = create_arrangement(layout)
    darr = create_domains_arr(arr, layout.domains)
    darr1 = place_nodes(darr)

    shapes = create_new_shapes(darr1)
    domains = create_new_domains(darr1)
    G = update_graph(shapes, layout.graph)

    return Layout(
        shapes=shapes,
        domains=domains,
        graph=G,
    )
