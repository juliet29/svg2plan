import networkx as nx
from copy import deepcopy

from classes.domains import DomainDict
from classes.directions import Direction
from placement.finder import Finder
from placement.updater import Updater
from placement.placer import Placer
from placement.interface import LooperInterface



class Looper(LooperInterface):
    def __init__(self, graph: nx.Graph, domains:DomainDict) -> None:
        self.G = deepcopy(graph)
        self.domains = deepcopy(domains)

        self.unplaced = list(self.G.nodes)

        self.tracker = {}
        self.tracker_row = 0
        self.tracker[self.tracker_row] = []

        self.curr_node = None
        self.nb = None

        self.finder = Finder(self)
        self.updater = Updater(self)
        self.placer = Placer(self)

    def run_ns_loop(self):
        self.ns_counter = 0
        while len(self.unplaced) > 0:
            if not self.finder.find_next_south_node():
                print("ns search failed, ending ns loop")
                break 

            self.placer.place_next_south_node()
            # finding for south nodes automatically updates curr_node
            
            self.updater.update_tracker()
            self.updater.update_unplaced()

            self.run_ew_loop()
            self.updater.update_tracker_row()

            if len(self.unplaced) == 0:
                print("no more nodes to place")
                break

            if self.is_over_ns_counter():
                print("ns_counter > 12 .. breaking")
                break


    def run_ew_loop(self):
        self.ew_counter = 0
        while True:
            if not self.finder.find_next_directed_node(Direction.WEST):
                print(f"---{self.curr_node} has no western nbs that are unplaced")
                return 
            else:
                print(f"next west node is {self.nb}")
                # placement requires knowledge of current and next.. 
                self.placer.place_next_west_node()

                self.updater.update_curr_node()
                self.updater.update_tracker()
                self.updater.update_unplaced()
                

            if self.is_over_ew_counter():
                print("ew_counter > 5 .. breaking")
                return


    def is_over_ns_counter(self):
        self.ns_counter+=1
        if self.ns_counter > 12:
            return True
        
    def is_over_ew_counter(self):
        self.ew_counter+=1
        if self.ew_counter > 5:
            return True











    









    
