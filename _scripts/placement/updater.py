class Updater:
    def __init__(self, looper_obj) -> None:
        self.lo = looper_obj
            # updates
    def update_curr_node(self):
        self.lo.curr_node = self.lo.nb
        

    def update_tracker(self):
        if self.lo.tracker_row not in self.lo.tracker.keys():
            self.lo.tracker[self.lo.tracker_row] = []
        self.lo.tracker[self.lo.tracker_row].append(self.lo.curr_node)

    def update_tracker_row(self):
        self.lo.tracker_row+=1
    
    def update_unplaced(self):
        self.lo.unplaced.remove(self.lo.curr_node)

