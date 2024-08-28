from placement.interface import LooperInterface

class Updater:
    def __init__(self, looper_obj:LooperInterface) -> None:
        self.lo = looper_obj
            # updates
    def update_curr_node(self):
        self.lo.curr_node = self.lo.nb
        

    def update_tracker(self):
        if self.lo.tracker_column not in self.lo.tracker.keys():
            self.lo.tracker[self.lo.tracker_column] = []
        self.lo.tracker[self.lo.tracker_column].append(self.lo.curr_node)

    def update_tracker_column(self):
        self.lo.tracker_column+=1
    
    def update_unplaced(self, node:str):
        self.lo.unplaced.remove(node)

