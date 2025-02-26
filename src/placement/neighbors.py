from decimal import Decimal
from turtle import pos
from sympy import EX
from domains.domain import Domain
from domains.range import Range
from helpers.directions import get_opposite_axis
from helpers.helpers import filter_none
from helpers.layout import DomainsDict


def get_possible_nbs(node: Domain, domains: DomainsDict, ax) -> list[Domain]:
    other_doms = list(set(domains.values()).difference(set([node])))
    assert not isinstance(node, str)
    ax2 = get_opposite_axis(ax)


    def is_possible_nb(other: Domain):
        return node[ax2].is_intersecting_shapely(other[ax2]) and node[ax].is_strictly_smaller(other[ax])

    poss_nbs = [i for i in other_doms if is_possible_nb(i)]
    return sorted(poss_nbs, key=lambda n: n[ax].min)


def create_ranges_between(
    node: Domain, poss_nbs: list[Domain], ax
) -> dict[str, Range]:
    
    def create_range(other: Domain):
        try:
            return Range(node[ax].max, other[ax].min)
        except:
            return Range(node[ax].max, node[ax].max)

    res = {}
    for i in poss_nbs:
        try:
            res[i.name] = create_range(i)
        except:
            print(node.name, i.name)
            raise Exception("ranges failed")
        
    res = {i.name: create_range(i) for i in poss_nbs}

        

    return res


def find_possible_nbs_and_ranges(node: Domain, domains: DomainsDict, ax):
    poss_nbs = get_possible_nbs(node, domains, ax)
    ranges = create_ranges_between(node, poss_nbs, ax)
    return poss_nbs, ranges


def find_adjacent_nodes(ranges: dict[str, Range], domains: DomainsDict, ax):

    def create_comparisons(poss_nbs: list[str]) -> list[list[str]]:
        comparisons = []
        for ix, _ in enumerate(poss_nbs):
            comparisons.extend([poss_nbs[: ix + 1]])
        return filter_none(comparisons)

    def is_seperated_by_another_node(comparison: list[str]):
        if len(comparison) == 1:
            return
        *others, current = comparison
        for other in others:
            if ranges[current].contains(domains[other][ax]):
                return True

    comparisons = create_comparisons((list(ranges.keys())))
    adjacent_nodes = []
    for cmp in comparisons:
        if not is_seperated_by_another_node(cmp):
            adjacent_nodes.append(cmp[-1])
        else:
            return adjacent_nodes
    return adjacent_nodes


def create_ranges_for_all_nodes(domains: DomainsDict, ax):
    def collect_adjacent_nodes(node: Domain):
        _, ranges = find_possible_nbs_and_ranges(node, domains, ax)
        nbs = find_adjacent_nodes(ranges, domains, ax)
        if nbs:
            return {k: v for k, v in ranges.items() if k in nbs}

    nb_ranges = {d.name: collect_adjacent_nodes(d) for d in domains.values()}
    return {k: v for k, v in nb_ranges.items() if v}
