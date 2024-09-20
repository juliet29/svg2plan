from __init__ import *
from runner.svg2plan import SVG2Plan
from log_setter.log_settings import logger
from new_corners.range import *
from new_corners.domain import *


def main():
    control = nonDecimalRange(10,20).toRange()
    narrower = nonDecimalRange(12, 18).toRange()
    wider = nonDecimalRange(8, 22).toRange()
    larger = nonDecimalRange(21, 23).toRange()
    smaller = nonDecimalRange(6, 7.5).toRange()
    smaller_overlap = nonDecimalRange(6, 10).toRange()


    north_domain = Domain(name="north", x=control, y=larger)
    south_domain = Domain(name="south", x=control, y=smaller)
    res = north_domain.compare_domains(south_domain)
    return res


if __name__=="__main__":
    main()