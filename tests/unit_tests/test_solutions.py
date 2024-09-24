from new_solutions.simple_problem import *
from new_solutions.selection import *
from runner.svg2plan import run_new_layout
import pytest



def test_best_sol_for_hole_in_amber_a():
    report = run_new_layout()
    sop = StudyOneProblem(*report.output, FilterDesc(ProblemType.HOLE, []))
    sop.run()
    bl = select_best_layout(sop.results)
    assert bl.summary["OVERLAP"] == 3


def test_best_sol_for_overlap_in_amber_a():
    report = run_new_layout()
    sop = StudyOneProblem(*report.output, FilterDesc(ProblemType.OVERLAP, ["m_closet", "dining"]))
    sop.run()
    bl = select_best_layout(sop.results)
    assert bl.summary["HOLE"] == 1
    assert bl.summary["OVERLAP"] == 2


# results = conduct_study()
report = run_new_layout()
output=init_let_it_cook(report, FilterDesc(ProblemType.OVERLAP, ["bath"]))
output = let_it_cook(output)