import pytest
from reader.svg_reader import SVGReader
from adjacencies.adjacency import AdjacencyGenerator
from placement.executer import PlacementExecuter


@pytest.fixture(params=["amber_a_f01.svg", "amber_b_f01.svg"])
def runner(request):
    sv = SVGReader(request.param)
    sv.run()
    ag = AdjacencyGenerator(sv.layout)
    ag.run()
    pl = PlacementExecuter(ag.layout)
    pl.run()
    return pl


def test_north_west_node_has_valid_nbs(runner):
    nw_node = runner.tracker[0][0]
    nbdata = runner.layout.graph.nodes[nw_node]["data"]
    assert not nbdata["NORTH"] and not nbdata["WEST"]


def test_all_rooms_in_tracker(runner):
    pl = runner
    rooms = set(pl.layout.corners.keys())
    tracker_rooms = set([room for arr in pl.tracker.values() for room in arr])
    assert tracker_rooms == rooms


def test_precision_of_corners(runner):
    for corner in runner.layout.corners.values():
        for num in corner:
            assert num.is_finite()
            if num >= 10 or num <= -10:
                assert len(num.as_tuple().digits) <= 4
            elif -10 < num < 10:
                assert len(num.as_tuple().digits) <= 3


def test_all_shapes_are_polygons(runner):
    for shape in runner.layout.shapes.values():
        assert len([i for i in shape.exterior.coords]) == 5
        assert len([i for i in shape.interiors]) == 0
