from placement.interface import LooperInterface

class Updater:
    def __init__(self, looper_obj:LooperInterface) -> None:
        self.lo = looper_obj
        

    def update_tracker(self):
        self.lo.tracker[self.lo.tracker_column] = []
        self.lo.tracker[self.lo.tracker_column].append(self.lo.curr_node)


    def extend_tracker_west(self):
        self.lo.tracker_column+=1
    
    
    def extend_tracker_south(self, column):
        column.append(self.lo.curr_node)


    def update_unplaced(self):
        self.lo.unplaced.remove(self.lo.curr_node)

    

