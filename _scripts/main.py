from __init__ import *
from actions.interfaces import CurrentDomains
from runner.svg2plan import SVG2Plan
from log_setter.log_settings import logger

from new_corners.range import nonDecimalRange, Range
from new_corners.domain import Domain
from actions.actions import Pull, Push, Stretch, Shrink, Details
from svg_helpers.directions import Direction


def main():
    a_x = nonDecimalRange(10,20).toRange()
    b_x = nonDecimalRange(20, 25).toRange()
    y = nonDecimalRange(10, 30).toRange()

    room = Domain(name="room", x=a_x, y=y)
    hole = Domain(name="hole", x=b_x, y=y)
    curr_doms = CurrentDomains(room, hole)

    pu = Pull(curr_doms)
    pu.get_details()
    pu.get_action_direction()
    pu.execute_action()

    return pu



if __name__=="__main__":
    main()
