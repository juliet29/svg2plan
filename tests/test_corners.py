from new_corners.range import nonDecimalRange
from new_corners.domain import Domain
import pytest

control = nonDecimalRange(10,20).toRange()
narrower = nonDecimalRange(12, 18).toRange()
wider = nonDecimalRange(8, 22).toRange()
larger = nonDecimalRange(21, 23).toRange()
smaller = nonDecimalRange(6, 7.5).toRange()
smaller_overlap = nonDecimalRange(6, 10).toRange()


north_domain = Domain(name="north", x=control, y=larger)
south_domain = Domain(name="south", x=control, y=smaller)

east_domain = Domain(name="east", x=larger, y=control)
west_domain = Domain(name="west", x=smaller, y=control)

east_north_domain = Domain(name="en", x=larger, y=larger)
west_south_domain = Domain(name="ws", x=smaller, y=smaller)

class TestDomain:
    def test_ns(self):
        res = north_domain.compare_domains(south_domain)
        assert res.NORTH == north_domain
        assert res.SOUTH == south_domain
        assert res.EAST == None
        assert res.WEST == None

    def test_ew(self):
        res = east_domain.compare_domains(west_domain)
        assert res.NORTH == None
        assert res.SOUTH == None
        assert res.EAST == east_domain
        assert res.WEST == west_domain


    def test_diagonal(self):
        res = east_north_domain.compare_domains(west_south_domain)
        assert res.NORTH == east_north_domain
        assert res.SOUTH == west_south_domain
        assert res.EAST == east_north_domain
        assert res.WEST == west_south_domain



class TestRange:
    # def test_overlaps(self):
    #     assert control.overlaps(narrower) 

    # def test_is_within(self):
    #     assert control.is_within(wider) 

    def test_is_smaller(self):
        assert control.is_smaller(larger) 

    def test_is_larger(self):
        assert control.is_larger(smaller) 

    def test_compared_gap(self):
        result = control.compare_ranges(larger)
        assert result is not None and result.Lesser == control

        result = control.compare_ranges(smaller)
        assert result is not None and result.Lesser == smaller

    def test_compared_overlap(self):
        result = control.compare_ranges(smaller_overlap)
        assert result is not None and result.Lesser == smaller_overlap

    def test_unomparable(self):
        result = control.compare_ranges(narrower)
        assert result.is_empty()



