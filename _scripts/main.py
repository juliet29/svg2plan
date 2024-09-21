from __init__ import *
from actions.interfaces import CurrentDomains
from runner.svg2plan import SVG2Plan
from log_setter.log_settings import logger

from reader.svg_reader import SVGReader
from adjacencies.adjacency import AdjacencyGenerator
from placement.executer import PlacementExecuter
from problems.reporter import Reporter
from svg_helpers.plotter import Plotter
from svg_helpers.saver import Saver
from new_solutions.simple_problem import *


def main():
    operations = execute_actions()
    return operations
    # sv = SVGReader("amber_a_f01.svg")
    # sv.run()
    # ag = AdjacencyGenerator(sv.domains)
    # ag.run()
    # pe = PlacementExecuter(ag.layout)
    # pe.run()
    # re = Reporter(pe.layout)
    # re.run()
    # s = Saver(re.layout, "amber_a_placed")
    # s.add_problems(re.problems)
    # s.save()
    # pl = Plotter(re.layout.corners, yrange=[1, -10])
    # pl.plot()


if __name__=="__main__":
    main()
