import numpy as np
from export.saver import read_pickle
from helpers.graph_helpers import sort_nodes_on_egde
from helpers.layout import Layout
from copy import deepcopy

# layout: Layout = read_pickle("1001_amber_c_ag")

def initialize_arr(layout: Layout):
    sd = sort_nodes_on_egde(layout.graph, layout.domains)
    arr = np.full(shape=(len(sd["WEST"]), len(sd["NORTH"])), fill_value="", dtype=object)
    north_row = np.s_[0, :]
    west_col = np.s_[:, 0]

    # place north nodes and west nodes
    arr[north_row] = [i.name for i in sd["NORTH"]]
    # arr[west_col] = [i.name for i in sd["WEST"]]
    return arr, sd, north_row, west_col

def get_unplaced(arr, domains):
    return set(domains.keys()).difference(set(np.unique(arr)))

def get_row(arr, ix):
    return list(arr[ix, :])

def is_north_nb_in_row(ix, node, G, arr):
    nodes_to_find = get_row(arr, ix)
    for i in G.nodes()[node]["data"]["NORTH"]:
        if i in nodes_to_find:
            return node

def get_next_row(ref_row, G, arr, domains, unplaced):
    res = [is_north_nb_in_row(ref_row, node, G, arr) for node in unplaced]
    valid_res = [i for i in res if i]
    return sorted(valid_res, key=lambda i: domains[i]["x"].min)

def get_next_row_all(ref_row, G, arr, domains, unplaced):
    res = [is_north_nb_in_row(ref_row, node, G, arr) for node in unplaced]
    valid_res = [i for i in res if i]
    return sorted(valid_res, key=lambda i: domains[i]["x"].min)

def adjust_arr_for_row(arr, row):
    n_rows, n_cols = arr.shape
    if n_cols < len(row):
        diff = len(row) - n_cols
        temp = np.full(shape=(n_rows, diff), fill_value="", dtype=object)
        narr = np.hstack((arr, temp))
        return narr
    return deepcopy(arr)

def update_arr(arr, row, ix):
    narr = deepcopy(arr)
    narr[ix, 0:len(row)] = row
    return narr

def get_current_row(arr):
    for ix, i in enumerate(arr):
        if not i.any():
            return ix - 1
    raise Exception("Couldnt find current row")
    
def place_next_row(G, domains, arr, unplaced):
    # TODO: compute ix automatically based on the last non-empty row.. 
    ix = get_current_row(arr)
    row = get_next_row(ix, G, arr, domains, unplaced)
    narr = adjust_arr_for_row(arr, row)
    return update_arr(narr, row, ix+1)





class ArrangementTracker:
    def __init__(self, layout) -> None:
        self.layout = layout
        self.graph = layout.graph
        self.domains = layout.domains
        self.max_iter = 10

    def init_arr(self):
        self.arr, *_ = initialize_arr(self.layout)


    def get_unplaced(self):
        self.unplaced = get_unplaced(self.arr, self.domains)

    def iterate(self):
        pass

    def run(self):
        self.init_arr()
        self.get_unplaced()
        self.counter = 0
        while self.unplaced:
            print(self.counter)
            self.arr = place_next_row(self.graph, self.domains, self.arr, self.unplaced)
            self.get_unplaced()
            self.counter+=1
            if self.counter > self.max_iter:
                raise Exception("Max iterations exceeded!")
            
        return self.arr

# at = ArrangementTracker(layout)
# at.run()