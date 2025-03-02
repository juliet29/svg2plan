from svg2plan.domains.range import InvalidRangeException, Range, nonDecimalRange
import pytest


class TestRange:

    @pytest.fixture(autouse=True)
    def get_control(self, control: Range):
        self._control = control

    @pytest.mark.parametrize(
        "larger, expected",
        [
            (nonDecimalRange(21, 24).toRange(), True),
            (nonDecimalRange(19, 23).toRange(), False),
        ]
    )
    def test_is_strictly_smaller(self, larger, expected):
        assert self._control.is_strictly_smaller(larger) == expected

    def test_is_smaller(self, larger: Range):
        assert self._control.is_smaller(larger)

    def test_is_larger(self, smaller: Range):
        assert self._control.is_larger(smaller)

    def test_compared_gap(self, larger: Range, smaller: Range):
        result = self._control.compare_ranges(larger)
        assert result.Lesser == self._control

        result = self._control.compare_ranges(smaller)
        assert result.Lesser == smaller

    def test_within_is_not_overlapping_larger(self):
        narrower = nonDecimalRange(12, 18).toRange()
        wider = nonDecimalRange(8, 22).toRange()
        assert not self._control.is_overlapping_and_larger(narrower)
        assert not self._control.is_overlapping_and_smaller(wider)

    def test_is_overlapping_and_larger(self):
        overlap_smaller = nonDecimalRange(8, 12).toRange()
        assert self._control.is_overlapping_and_larger(overlap_smaller)

    def test_is_overlapping_and_larger_edge(self):
        overlap_smaller_edge = nonDecimalRange(10, 15).toRange()
        assert self._control.is_overlapping_and_larger(overlap_smaller_edge)

    def test_is_overlapping_and_smaller_edge(self):
        overlap_larger_edge = nonDecimalRange(12, 20).toRange()
        assert self._control.is_overlapping_and_smaller(overlap_larger_edge)

    def test_is_overlapping_and_smaller(self):
        overlap_larger = nonDecimalRange(14, 24).toRange()
        assert self._control.is_overlapping_and_smaller(overlap_larger)

    def test_compared_touching(self):
        smaller_touching = nonDecimalRange(6, 10).toRange()
        result = self._control.compare_ranges(smaller_touching)
        assert result.Lesser == smaller_touching

    def test_compare_overlapping_ranges(self):
        overlap_larger = nonDecimalRange(14, 24).toRange()
        overlap_smaller = nonDecimalRange(8, 12).toRange()
        result = self._control.compare_ranges(overlap_larger, consider_overlap=True)
        assert result.Lesser == self._control

        result = self._control.compare_ranges(overlap_smaller, consider_overlap=True)
        assert result.Lesser == overlap_smaller

    def test_uncomparable(self):
        narrower = nonDecimalRange(12, 18).toRange()
        result = self._control.compare_ranges(narrower)
        assert result.is_empty()

    def test_other_side(self):
        res = self._control.get_other_side("min")
        assert res == "max"

    def test_invalid_range(self):
        with pytest.raises(InvalidRangeException):
            nonDecimalRange(10, 1).toRange()

    def test_zero_width_range_is_valid(self):
        # with pytest.raises(InvalidRangeException):
        assert nonDecimalRange(1, 1).toRange()

    def test_modification(self):
        def fx(x):
            return x + 2

        res = self._control.modify(fx)
        assert res.min == self._control.min + 2
        assert res.max == self._control.max + 2

    @pytest.mark.parametrize(
        "min, max, expected",
        [
            pytest.param(20, 25, False, id="touch_at_one_point"),
            pytest.param(22, 25, False, id="disjoint"),
            pytest.param(15, 25, True, id="intersecting"),
        ],
    )
    def test_shapely_intersecting(self, min: int, max: int, expected: bool):
        other = nonDecimalRange(min, max).toRange()
        assert self._control.is_intersecting_shapely(other) == expected
