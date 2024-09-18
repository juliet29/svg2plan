import pytest
from reader.svg_reader import SVGReader
from adjacencies.adjacency import AdjacencyGenerator
from placement.executer import PlacementExecuter
from problems.reporter import Reporter
from problems.classes.sequence import Sequence
from problems.sequence_runner import SequenceRunner

@pytest.fixture(params=["amber_a_f01.svg", "amber_b_f01.svg"])
def runner(request):
    sv = SVGReader(request.param)
    sv.run()
    ag = AdjacencyGenerator(sv.domains)
    ag.run()
    pe = PlacementExecuter(ag.layout)
    pe.run()
    re = Reporter(pe.layout)
    re.run()
    seq = Sequence(0, pe.layout, re.problems, [])
    sr = SequenceRunner(seq, re.problems[0])
    sr.run()
    return sr


# @pytest.mark.skip(reason="init is breaking")
def test_no_problems_in_final_layout(runner):
    re2 = Reporter(runner.layout)
    re2.run()
    assert len(re2.problems) == 0

@pytest.mark.skip(reason="init is breaking")
def test_correct_num_digits(runner):
    pass

@pytest.mark.skip(reason="init is breaking")
def test_precision_of_corners(runner):
    for corner in runner.layout.corners.values():
        for num in corner:
            assert num.is_finite()
            if num >= 10 or num <= -10:
                assert len(num.as_tuple().digits) <= 4
            elif -10 < num < 10: 
                assert len(num.as_tuple().digits) <= 3


