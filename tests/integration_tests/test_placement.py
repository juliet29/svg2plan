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
    rooms = set(pl.layout.domains.keys())
    tracker_rooms = set([room for arr in pl.tracker.values() for room in arr])
    assert tracker_rooms == rooms


def test_shapes_are_all_rectangles(runner):
    sv = runner
    for shape in sv.layout.shapes.values():
        assert len([i for i in shape.exterior.coords]) == 5

def test_precision_of_domains(runner):
    for domain in runner.layout.domains.values():
        for num in domain.get_values():
            assert num.is_finite()
            if num >= 10 or num <= -10:
                assert len(num.as_tuple().digits) <= 4
            elif -10 < num < 10: 
                assert len(num.as_tuple().digits) <= 3
