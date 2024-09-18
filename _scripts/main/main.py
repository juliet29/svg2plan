import os 
import logging
from reader.svg_reader import SVGReader
from adjacencies.adjacency import AdjacencyGenerator
from adjacencies.connectivity import ConnectivityGenerator
from placement.executer import PlacementExecuter

from problems.reporter import Reporter
from problems.classes.sequence import Sequence
from problems.sequence_runner import SequenceRunner
from problems.side_leveler import SideLeveler

from svg_helpers.gplan_creator import GPLANCreator
from svg_helpers.plotter import Plotter


logging.basicConfig(filename='test.log', encoding='utf-8', level=logging.DEBUG, format="%(levelno)s:%(module)s> %(message)s", filemode="w")

class SVG2Plan:
    def __init__(self, svg_name: str, folder_name: str) -> None:
        self.svg_name = svg_name
        self.folder_name = folder_name
        self.prepare_folder()

    def run(self):
        self.read_in_svg()
        self.stack_rooms()
        self.fix_problems()
        self.save_plan()

    def prepare_folder(self):
        self.path = path = os.path.join("../outputs/", self.folder_name)
        if not os.path.exists(path):
            os.makedirs(path)

    def read_in_svg(self):
        self.sv = SVGReader(self.svg_name)
        self.sv.run()

        self.ag = AdjacencyGenerator(self.sv.domains, 0.4)
        self.ag.run()

        # self.cg = ConnectivityGenerator(self.ag.positioned_graph, self.folder_name)
        # self.cg.run() #TODO need to pause and probs make this interactive.. 

    def stack_rooms(self):
        self.pe = PlacementExecuter(self.ag.layout)
        self.pe.run()


    def fix_problems(self):
        self.re = Reporter(self.pe.layout)
        self.re.run()
        self.seq = Sequence(0, self.pe.layout, self.re.problems, [])
        self.sr = SequenceRunner(self.seq, self.re.problems[0])
        self.sr.run()

        self.sl = SideLeveler(self.sr.layout)
        self.sl.run()

    def save_plan(self):
        self.gp = GPLANCreator(self.sl.corners, self.folder_name)
        self.gp.run()


    def plot_object_corners(self, corners, is_top: bool=False):
        if is_top:
            yrange=[-1, 14]
        else:
            yrange=[-14, 1]
        self.pl = Plotter(corners, yrange=yrange)
        self.pl.plot()
        