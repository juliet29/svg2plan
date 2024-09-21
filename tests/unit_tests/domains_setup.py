from new_corners.domain import Domain
from new_corners.range import nonDecimalRange
from decimal import Decimal

dec = Decimal(3)

control = nonDecimalRange(10, 20).toRange()
overlap_larger = nonDecimalRange(14, 24).toRange()
overlap_smaller = nonDecimalRange(8, 12).toRange()
narrower = nonDecimalRange(12, 18).toRange()
wider = nonDecimalRange(8, 22).toRange()
larger = nonDecimalRange(21, 23).toRange()
smaller = nonDecimalRange(6, 7.5).toRange()
smaller_touching = nonDecimalRange(6, 10).toRange()

north_domain = Domain(name="north", x=control, y=larger)
south_domain = Domain(name="south", x=control, y=smaller)

east_domain = Domain(name="east", x=larger, y=control)
west_domain = Domain(name="west", x=smaller, y=control)

east_north_domain = Domain(name="en", x=larger, y=larger)
west_south_domain = Domain(name="ws", x=smaller, y=smaller)
