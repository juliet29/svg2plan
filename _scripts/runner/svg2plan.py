import os
import logging
import json
from read.svg_reader import SVGReader
from adjacencies.adjacency import AdjacencyGenerator
from adjacencies.connectivity import ConnectivityGenerator
from placement.executer import PlacementExecuter
from export.saver import Saver

from fixes.reporter import Reporter
# from problems.classes.sequence import Sequence
# from problems.sequence_runner import SequenceRunner
# from problems.side_leveler import SideLeveler

from export.gplan_creator import GPLANCreator
from visuals.plotter import Plotter

from svg_logger.settings import svlogger


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

def semi_run():
    re = run_new_layout()
    re = save_new_layout(re)





class SVG2Plan:
    def __init__(self, svg_name: str, folder_name: str) -> None:
        svlogger.info("Starting SVG2Plan \n ")
        self.svg_name = svg_name
        self.folder_name = folder_name
        self.prepare_folder()

    def run(self):
        self.read_in_svg()
        self.stack_rooms()
        self.fix_problems()
        # self.save_plan()

    def prepare_folder(self):
        self.path = path = os.path.join("../outputs/", self.folder_name)
        if not os.path.exists(path):
            os.makedirs(path)

    def read_in_svg(self):
        self.sv = SVGReader(self.svg_name)
        self.sv.run()

        self.ag = AdjacencyGenerator(self.sv.layout, 0.4)
        self.ag.run()

        # self.cg = ConnectivityGenerator(self.ag.positioned_graph, self.folder_name)
        # self.cg.run() #TODO need to pause and probs make this interactive..

    def stack_rooms(self):
        self.pe = PlacementExecuter(self.ag.layout)
        self.pe.run()

    def fix_problems(self):
        pass
        # self.re = Reporter(self.pe.layout)
        # self.re.run()
        # self.seq = Sequence(0, self.pe.layout, self.re.problems, [])
        # self.sr = SequenceRunner(self.seq, self.re.problems[0])
        # self.sr.run()

        # self.sl = SideLeveler(self.sr.layout)
        # self.sl.run()

    # def save_plan(self):
    #     self.gp = GPLANCreator(self.sl.corners, self.folder_name)
    #     self.gp.run()

    # def plot_object_corners(self, corners, is_top: bool = False):
    #     if is_top:
    #         yrange = [-1, 14]
    #     else:
    #         yrange = [-14, 1]
    #     self.pl = Plotter(corners, yrange=yrange)
    #     self.pl.plot()
