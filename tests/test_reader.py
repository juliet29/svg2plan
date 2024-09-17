import pytest
from reader.svg_reader import SVGReader

@pytest.fixture(params=["amber_a_f01.svg", "amber_b_f01.svg"])
def svg_reader(request):
    sv = SVGReader(request.param)
    sv.run()
    return sv

def test_at_least_one_corner(svg_reader):
    assert len(svg_reader.domains.corners) > 1

def test_equal_num_rectangles_and_corners(svg_reader):
    sv = svg_reader
    assert len(sv.domains.corners) == len(sv.rectangles)

def test_equal_num_rectangles_and_shapes(svg_reader):
    sv = svg_reader
    assert len(sv.domains.corners) == len(sv.domains.shapes)

def test_shapes_are_all_polygons(svg_reader):
    sv = svg_reader
    for shape in sv.domains.shapes.values():
        assert shape.exterior

def test_shapes_are_all_rectangles(svg_reader):
    sv = svg_reader
    for shape in sv.domains.shapes.values():
        assert len([i for i in shape.exterior.coords]) == 5

