from export.saver import read_pickle
from helpers.layout import Layout
from placement2.attract import *
import numpy as np
from read.svg_reader import SVGReader


def set_up_case(case):
    sv = SVGReader(case)
    sv.run()
    return sv.layout.domains

def test_a():
    case  = "amber_a_f01.svg"
    doms = set_up_case(case)
    n_doms = adjust_domains_x(doms)
    assert n_doms.keys() == doms.keys()

def test_b():
    case  = "amber_b_f01.svg"
    doms = set_up_case(case)
    n_doms = adjust_domains_x(doms)
    assert n_doms.keys() == doms.keys()

def test_c():
    case  = "amber_c_f01.svg"
    doms = set_up_case(case)
    n_doms = adjust_domains_x(doms)
    assert n_doms.keys() == doms.keys()
