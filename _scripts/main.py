from __init__ import *
from actions.interfaces import CurrentDomains
from log_setter.log_settings import svlogger

from reader.svg_reader import SVGReader
from adjacencies.adjacency import AdjacencyGenerator
from placement.executer import PlacementExecuter
from problems.reporter import Reporter
from svg_helpers.plotter import Plotter
from svg_helpers.saver import Saver
from new_solutions.simple_problem import *


def run_new_layout():
    sv = SVGReader("amber_a_f01.svg")
    sv.run()
    ag = AdjacencyGenerator(sv.layout)
    ag.run()
    pe = PlacementExecuter(ag.layout)
    pe.run()
    re = Reporter(pe.layout)
    re.run()
    return re


def save_new_layout(re):
    s = Saver(re.layout, "amber_a_placed")
    s.add_problems(re.problems)
    s.save()

def plot(re):
    plt = Plotter(re.layout.domains)
    plt.plot()





if __name__ == "__main__":
    re = run_new_layout()
    plot(re)

