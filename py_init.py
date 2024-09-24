#! /usr/bin/env python
import sys
sys.path.append("/Users/julietnwagwuume-ezeoke/_UILCode/gqe-phd/svg2plan/_scripts")
sys.path.append("/Users/julietnwagwuume-ezeoke/_UILCode/gqe-phd/svg2plan/tests")
from domains.domain import Domain
from domains.range import *
from domains.domain import *
from copy import deepcopy, copy
from importlib import reload
from pprint import pprint
from visuals.plotter import Plotter
from typing import Dict

from fixes.problem_types.side_hole_id2 import *


def plot_general(domains: Dict[str, Domain]):
    plt = Plotter(domains)
    plt.plot()



def main():
    pass
    


if __name__ == '__main__':
    # main should return 0 for success, something else (usually 1) for error.
    sys.exit(main())


# bpython -i py_init.py
# ipython -i py_init.py
