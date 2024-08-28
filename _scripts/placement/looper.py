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
        self.tracker_column = 0
        # self.tracker[self.tracker_column] = []

        self.curr_node = ""
        self.nb = ""

        self.finder = Finder(self)
        self.updater = Updater(self)
        self.placer = Placer(self)

    def run(self):
        self.set_north_east_node()
        self.run_ew_loop()
        self.set_relative_south_nodes()

    def set_north_east_node(self):
        self.finder.find_north_east_node()
        self.placer.place_north_east_node()
        self.tracker[self.tracker_column] = []
        self.tracker[self.tracker_column].append(self.curr_node)
        self.updater.update_unplaced(self.curr_node)



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
                self.tracker_column+=1
                self.tracker[self.tracker_column] = []
                self.tracker[self.tracker_column].append(self.curr_node)

                # self.updater.update_tracker()
                self.updater.update_unplaced(self.curr_node)
                

            if self.is_over_ew_counter():
                print("ew_counter > 5 .. breaking")
                return
            
    def set_relative_south_nodes(self):
        self.ns_counter = 0
        north_node_reference = 0
        while len(self.unplaced) > 0:
            for k, v in self.tracker.items():
                try:
                    north_node = v[north_node_reference]
                except:
                    print(f"north node = {north_node}. getting index {north_node_reference} in {v} failed")
                    break
                # sets the nb
                result = self.finder.find_next_directed_node(Direction.SOUTH, north_node)
                if result == True: 
                    print(f"{self.nb} is south of {north_node}")
                    # updating tracker
                    v.append(self.nb)
                    # have to place node TODO
                    # curr node doesnt matter anymore.. => should do away with nb rhetoric TODO
                    self.updater.update_unplaced(self.nb)

                if len(self.unplaced) == 0:
                    print("no more nodes to place")
                    return
                
            north_node_reference+=1
            print(f"changing north node reference to {north_node_reference}. Number of unplaced nodes is {len(self.unplaced)}")

            if self.is_over_ns_counter():
                print("ns_counter > 4 .. breaking")
                break




    def is_over_ns_counter(self):
        self.ns_counter+=1
        if self.ns_counter > 4:
            return True
        
    def is_over_ew_counter(self):
        self.ew_counter+=1
        if self.ew_counter > 5:
            return True







    # def run_ns_loop(self):
    #     self.ns_counter = 0
    #     while len(self.unplaced) > 0:
    #         if not self.finder.find_next_south_node():
    #             print("ns search failed, ending ns loop")
    #             break 

    #         self.placer.place_next_south_node()
    #         # finding for south nodes automatically updates curr_node
            
    #         self.updater.update_tracker()
    #         self.updater.update_unplaced()

    #         self.run_ew_loop()
    #         self.updater.update_tracker_row()








    









    
