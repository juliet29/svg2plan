from __init__ import *
from runner.svg2plan import SVG2Plan
from log_setter.log_settings import logger
from new_corners.range import *



def main():
    a = nonDecimalRange(1,2).toRange()
    print(a)


if __name__=="__main__":
    main()