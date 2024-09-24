from adjacencies.adjacency import AdjacencyGenerator
from domains.domain import Domain
from domains.range import Range
from fixes.problem_types.side_hole_id2 import check_for_side_holes
from helpers.helpers import pairwise
from helpers.layout import Layout, PartialLayout
from helpers.shapely import domain_to_shape

from decimal import Decimal
from itertools import chain, filterfalse, pairwise, product

s_hole = lambda i: (i.x.min == 1 and i.y.min == 0)
n_hole = lambda i: (i.x.min == 1 and i.y.min == 3)
e_hole = lambda i: (i.x.min == 3 and i.y.min == 1)
w_hole = lambda i: (i.x.min == 0 and i.y.min == 1)
holes = [s_hole, n_hole, e_hole, w_hole]

sols = {
    "w": (w_hole, (0, 1)),
    "s": (s_hole, (0, 4)),
    "e": (e_hole, (12, 13)),
    "n": (n_hole, (3, 7)),
}

def test_side_holes():
    for k,v in sols.items():
        sh = SideHoleSetup(k)
        sh.run()
        assert sh.res[0] == v[1]


class SideHoleSetup:
    def __init__(self, case: str = "w") -> None:
        prob = sols[case]
        self.filter_fx = prob[0]

    def run(self):
        # TODO -> first two are the same for all cases 
        self.begin()
        self.create_graph()
        self.create_filtered_layout()
        self.check_for_holes()

    def begin(self):
        xs = list((min, max) for min, max in pairwise(range(5)))
        res = list(product(xs, xs))
        self.domains = [
            Domain.create_domain(list(chain.from_iterable(i)), str(ix))
            for ix, i in enumerate(res)
        ]
        self.init_dict = {v.name: v for v in self.domains}


    def create_graph(self):
        self.shapes = {
            domain.name: domain_to_shape(domain) for domain in self.init_dict.values()
        }
        p = PartialLayout(self.shapes, self.init_dict)
        ag = AdjacencyGenerator(p, 0)
        ag.run()
        self.G = ag.G

    def create_filtered_layout(self):
        self.hole_domains = list(filterfalse(self.filter_fx, self.domains))
        gap = Decimal("0.2")
        odd: Domain = list(filter(self.filter_fx, self.domains))[0]
        rep_domain = Domain(
            Range(odd.x.min + gap, odd.x.max),
            Range(odd.y.min + gap, odd.y.max),
            name=odd.name,
        )
        self.hole_domains.append(rep_domain)
        self.hole_dict = {v.name: v for v in self.hole_domains}
        self.test_layout = Layout(self.shapes, self.hole_dict, self.G)

    def check_for_holes(self):
        self.pairs = list(check_for_side_holes(self.test_layout))
        self.res = [(int(i[0].name), int(i[1].name)) for i in self.pairs]


