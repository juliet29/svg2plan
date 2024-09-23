from networkx import Graph
from new_corners.domain import Domain
from helpers.directions import Direction, get_opposite_direction


def generate_directed_adjacencies(G: Graph, domain_a: Domain, domain_b: Domain):
    cmp = domain_a.compare_domains(domain_b)
    for drn in [Direction.NORTH, Direction.EAST]:
        opp_drn = get_opposite_direction(drn)
        if cmp[drn.name]:
            d1, d2 = (
                (domain_a, domain_b)
                if cmp[drn.name] == domain_a
                else (domain_b, domain_a)
            )
            G.nodes[d1.name]["data"][opp_drn.name].append(d2.name)
            G.nodes[d2.name]["data"][drn.name].append(d1.name)

    return G
