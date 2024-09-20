from __init__ import *
from runner.svg2plan import SVG2Plan
from log_setter.log_settings import logger

from new_corners.range import nonDecimalRange, Range
from new_corners.domain import Domain
from actions.actions import Pull, Push, Stretch, Shrink, Details
from svg_helpers.directions import Direction


def main():
    a_x = nonDecimalRange(10,20).toRange()
    b_x = nonDecimalRange(21, 25).toRange()
    y = nonDecimalRange(10, 30).toRange()

    room = Domain(name="room", x=a_x, y=y)
    hole = Domain(name="hole", x=b_x, y=y)

    d = Details(node_domain=room, problem_domain=hole)
    return d


if __name__=="__main__":
    main()
