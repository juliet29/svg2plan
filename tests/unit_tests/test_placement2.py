from export.saver import read_pickle
from helpers.layout import Layout
from placement2.arrange import create_placement




def expected_placement():
    layout: Layout = read_pickle("1001_amber_c_ag")
    d = layout.domains
    d0 = [d["m_bed"], d["bed1"]]
    d1 = [d["m_closet"], d["transit"], d["bed1_closet"]]
    d2 = [d["m_bath"], d["corridor"], d["linen"], d["linen"]]
    d3 = [d["bath"], d["den"]]
    d4 = [d["kitchen"], d["dining"], d["den_closet"]]
    d5 = [d["living"]]

    return [[i.name for i in g] for g in [d0, d1, d2, d3, d4, d5]]

def test_expected_placement():
    layout: Layout = read_pickle("1001_amber_c_ag")
    assert expected_placement() == create_placement(layout)