from functools import reduce
from itertools import pairwise, product
from operator import add
from numpy import isin
from domains.range import Range
from helpers.helpers import filter_none
from helpers.layout import DomainsDict, Layout, PartialLayout, OptionalDomainsDict
from domains.domain import Domain
import networkx as nx


def init_new_domains_dict(domains: DomainsDict):
    return {k: None for k in domains.keys()}


def get_possible_nbs_east(node: Domain, domains: DomainsDict) -> list[Domain]:
    other_doms = list(set(domains.values()).difference(set([node])))
    assert not isinstance(node, str)

    def is_possible_east_nb(other: Domain):
        return node.y.line_string_y.intersection(other.y.line_string_y) and other.x.min >= node.x.max

    poss_nbs = [i for i in other_doms if is_possible_east_nb(i)]
    return sorted(poss_nbs, key=lambda n: n.x.min)


def create_ranges_between_east(node: Domain, poss_nbs: list[Domain]) -> dict[str, Range]:
    def create_range(other: Domain):
        return Range(node.x.max, other.x.min)
    return {i.name: create_range(i) for i in poss_nbs}

def find_possible_east_nbs_and_ranges(node: Domain, domains: DomainsDict):
    poss_nbs = get_possible_nbs_east(node, domains)
    ranges = create_ranges_between_east(node, poss_nbs)
    return poss_nbs, ranges


def create_comparisons(poss_nbs: list[str]) -> list[list[str]]:
    comparisons = []
    for ix, _ in enumerate(poss_nbs):
        comparisons.extend([poss_nbs[:ix+1]])
    return filter_none(comparisons)


def find_adjacent_nodes(
    ranges: dict[str, Range], domains: DomainsDict
):
    def is_seperated_by_another_node(comparison: list[str]):
        if len(comparison) == 1:
            return
        *others, current = comparison
        for other in others:
            if ranges[current].contains(domains[other].x):
                return True

    comparisons = create_comparisons((list(ranges.keys())))
    adjacent_nodes = []
    for cmp in comparisons:
        if not is_seperated_by_another_node(cmp):
            adjacent_nodes.append(cmp[-1])
        else:
            return adjacent_nodes
    return adjacent_nodes
        
def collect_adjacent_nodes(node: Domain, domains: DomainsDict):
    poss_nbs, ranges = find_possible_east_nbs_and_ranges(node, domains)
    nbs = find_adjacent_nodes(ranges, domains)
    if nbs:
        return {k:v for k,v in ranges.items() if k in nbs}
    



def create_ranges_for_all_nodes(domains: DomainsDict):
    nb_ranges = {d.name:collect_adjacent_nodes(d, domains) for d in domains.values()}
    return {k:v for k,v in nb_ranges.items() if v}

def create_graph(domains: DomainsDict):
    ranges = create_ranges_for_all_nodes(domains)
    G = nx.DiGraph()
    for k,v in ranges.items():
        n1 = k
        for k1, v1 in v.items():
            n2 = k1
            G.add_edge(n1, n2, size=v1.size)
    return G

    # TODO check that is acyclic and directed




def get_distances(G: nx.DiGraph):
    def segment_roots():
        roots = [n[0] for n in G.in_degree if n[1] == 0]
        non_roots = [n[0] for n in G.in_degree if n[1] != 0]
        return list(product(roots, non_roots))

    def get_paths(root, node):
        return [i for i in nx.all_simple_paths(G, root, node)]

    def get_size_of_path(path: list[str]):
        return reduce(add, [G.edges[u,v]["size"] for u,v in pairwise(path)])
    
    sizes = []
    for pair in segment_roots():
        paths = get_paths(*pair)
        if paths:
            sz = min([get_size_of_path(p) for p in paths])
            sizes.append((*pair, sz))

    return sizes



    



## drawing 

def create_pos(domains):
    return {k:( float(v.x.min), float(v.y.min))for k,v in domains.items()}

def draw_digraph(G, pos):
    nx.draw(G, pos=pos)
    nx.draw_networkx_labels(G,pos, labels={n: n for n in G},font_size=10)
    edge_labels = nx.get_edge_attributes(G, 'size')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)