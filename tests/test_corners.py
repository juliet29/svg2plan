from tests.domains_setup import *
import pytest
from new_corners.range import create_modfified_range
from operator import add, sub
from decimal import Decimal


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

    def test_get_other_axis(self):
        assert north_domain.get_other_axis("y") == "x"



class TestRange:
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

    def test_uncomparable(self):
        result = control.compare_ranges(narrower)
        assert result.is_empty()

    def test_other_side(self):
        res = control.get_other_side("min")
        assert res == "max"


    def test_modifing_range(self):
        mod = create_modfified_range(control, dec, sub,)
        assert mod.min == control.min - dec
        assert mod.max == control.max - dec 

    def test_modifing_range_single_side(self):
        mod = create_modfified_range(control, dec, add, "min")
        assert mod.min == control.min + dec





