import pytest

from reader.svg_reader import SVGReader
from adjacencies.adjacency import AdjacencyGenerator


@pytest.fixture(params=["amber_a_f01.svg", "amber_b_f01.svg"])
def runner(request):
    sv = SVGReader(request.param)
    sv.run()
    ag = AdjacencyGenerator(sv.layout)
    ag.run()
    return ag


def test_for_complete_layout_object(runner):
    assert runner.layout.shapes and runner.layout.corners and runner.layout.graph


def test_num_graph_nodes_equals_num_corners(runner):
    assert len(runner.layout.shapes) == len(runner.layout.graph.nodes)


def test_some_edges_exist(runner):
    assert len(runner.layout.graph.edges) > 0


def test_neighbors_are_directed(runner):
    G = runner.layout.graph
    for _, attrs in G.nodes(data=True):
        assert len(attrs["data"]["NORTH"]) >= 0
