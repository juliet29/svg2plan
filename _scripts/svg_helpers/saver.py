from svg_helpers.layout import Layout
import pickle
import os

class Saver():
    def __init__(self, layout:Layout, file_name) -> None:
        self.layout = layout
        self.file_name = file_name
        self.path = os.path.join("../intermediate_solutions/", f"{self.file_name}.pickle")

    def save(self):
        with open(self.path, 'wb') as handle:
            pickle.dump(self.layout, handle, protocol=pickle.HIGHEST_PROTOCOL)


def read_layout(file_name):
    path = os.path.join("../intermediate_solutions/", f"{file_name}.pickle")
    with open(path, 'rb') as handle:
        layout = pickle.load(handle)

    return layout


