from domains.domain import Domain
from helpers.directions import Direction
from decimal import Decimal

class DomainComparisonError(Exception):
    def __init__(self, domains: tuple[Domain, Domain]):            
        super().__init__("Problem domains should have a relationship!")
            
        # print(domains)


def get_problem_size(prob_domain: Domain, drn: Direction) -> Decimal:
    match drn:
        case Direction.NORTH | Direction.SOUTH:
            return prob_domain.y.size
        case Direction.EAST | Direction.WEST:
            return prob_domain.x.size
        case _:
            raise Exception("Invalid axis")


def get_domain_directions(a: Domain, b: Domain, consider_overlap=True):
    cmp = a.compare_domains(b, consider_overlap)
    if cmp.is_empty():
        cmp = b.compare_domains(a, consider_overlap)
    if cmp.is_empty():
        return None
        # raise DomainComparisonError((a,b))
    return cmp
