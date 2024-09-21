import pytest
from reader.svg_reader import SVGReader

@pytest.fixture(params=["amber_a_f01.svg", "amber_b_f01.svg"])
def runner(request):
    sv = SVGReader(request.param)
    sv.run()
    return sv

def test_at_least_one_corner(runner):
    assert len(runner.domains.corners) > 1

def test_equal_num_rectangles_and_corners(runner):
    sv = runner
    assert len(sv.domains.corners) == len(sv.rectangles)

def test_equal_num_rectangles_and_shapes(runner):
    sv = runner
    assert len(sv.domains.corners) == len(sv.domains.shapes)

def test_shapes_are_all_polygons(runner):
    sv = runner
    for shape in sv.domains.shapes.values():
        assert shape.exterior

def test_shapes_are_all_rectangles(runner):
    sv = runner
    for shape in sv.domains.shapes.values():
        assert len([i for i in shape.exterior.coords]) == 5

def test_precision_of_corners(runner):
    for corner in runner.domains.corners.values():
        for num in corner:
            assert num.is_finite()
            if num >= 10 or num <= -10:
                assert len(num.as_tuple().digits) <= 4
            elif -10 < num < 10: 
                assert len(num.as_tuple().digits) <= 3


# TODO 
# test that in units of meters, that all decimals only have two vals of precision 
