from itertools import chain
from domains.domain import Domain
from helpers.directions import Direction
from decimal import Decimal

def chain_flatten(lst: list[list]):
    return list(chain.from_iterable(lst))

def get_problem_size(prob_domain: Domain, drn: Direction) -> Decimal:
    match drn:
        case Direction.NORTH | Direction.SOUTH:
            return prob_domain.y.size
        case Direction.EAST | Direction.WEST:
            return prob_domain.x.size
        case _:
            raise Exception("Invalid axis")
        
def get_domain_directions(a: Domain, b: Domain):
    cmp = a.compare_domains(b, consider_overlap=True)
    if cmp.is_empty():
        cmp = b.compare_domains(a, consider_overlap=True)
    if cmp.is_empty():
        raise Exception("Overlapping domains should have a relationship!")
    return cmp
