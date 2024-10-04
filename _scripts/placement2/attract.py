from numpy import isin
from domains.range import Range
from helpers.helpers import filter_none
from helpers.layout import DomainsDict, Layout, PartialLayout, OptionalDomainsDict
from domains.domain import Domain


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
    



def attract_to_node_east(
    node: Domain, domains: DomainsDict, new_domains: OptionalDomainsDict
) -> OptionalDomainsDict:
    cmp = node.x.max

    return new_domains
