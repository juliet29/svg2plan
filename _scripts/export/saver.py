from typing import Any
from helpers.layout import Layout
import pickle
import os
from identify.interfaces import Problem

PATH_TO_SOLS = (
    "/Users/julietnwagwuume-ezeoke/_UILCode/gqe-phd/svg2plan/intermediate_solutions"
)


class Saver:
    def __init__(self, layout: Layout, file_name) -> None:
        self.layout = layout
        self.file_name = file_name
        self.path = os.path.join(PATH_TO_SOLS, f"{self.file_name}.pickle")

    def add_problems(self, problems: list[Problem]):
        self.layout.problems = problems  # type: ignore

    def save(self):
        with open(self.path, "wb") as handle:
            pickle.dump(self.layout, handle, protocol=pickle.HIGHEST_PROTOCOL)


def read_pickle(path=None, file_name=None):
    if not path:
        assert file_name
        path = os.path.join(PATH_TO_SOLS, f"{file_name}.pickle")
    with open(path, "rb") as handle:
        obj = pickle.load(handle)
    return obj


def write_pickle(obj, file_name=None, path=None):
    if not path:
        assert file_name
        path = os.path.join(PATH_TO_SOLS, f"{file_name}.pickle")
    with open(path, "wb") as handle:
        pickle.dump(obj, handle, protocol=pickle.HIGHEST_PROTOCOL)
    return file_name
