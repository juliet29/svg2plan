import pytest
from new_corners.range import nonDecimalRange, Range
from new_corners.domain import Domain
from actions.actions import ExecuteAction
from actions.interfaces import ActionType
from actions.details import Details
from svg_helpers.directions import Direction
from actions.interfaces import CurrentDomains


# TODO right now only testing wes!

x_low = nonDecimalRange(10, 20).toRange()
x_high = nonDecimalRange(20, 25).toRange()
y_low = nonDecimalRange(10, 40).toRange()
y_high = nonDecimalRange(40, 80).toRange()

room = Domain(name="room", x=x_low, y=y_low)
hole = Domain(name="hole", x=x_high, y=y_low)
WE_doms = CurrentDomains(room, hole)
d = Details(WE_doms)

room_ns = Domain(name="room", x=x_low, y=y_high)
hole_ns = Domain(name="hole", x=x_low, y=y_low)
NS_doms = CurrentDomains(room_ns, hole_ns)


class TestDetailsW:
    def test_relative_direction(self):
        d = Details(WE_doms)
        assert d.relative_direction == Direction.WEST

    def test_problem_size(self):
        d = Details(WE_doms)
        assert d.problem_size == x_high.size


class TestActionsW:
    def test_stretch(self):
        ea = ExecuteAction(WE_doms, ActionType.STRETCH)
        assert ea.modified_domain.x == Range(room.x.min, room.x.max + d.problem_size)

    def test_squeeze(self):
        ea = ExecuteAction(WE_doms, ActionType.SQUEEZE)
        assert ea.modified_domain.x == Range(room.x.min, room.x.max - d.problem_size)

    def test_push(self):
        ea = ExecuteAction(WE_doms, ActionType.PUSH)
        assert ea.modified_domain.x == Range(
            room.x.min - d.problem_size, room.x.max - d.problem_size
        )

    def test_pull(self):
        ea = ExecuteAction(WE_doms, ActionType.PULL)
        assert ea.modified_domain.x == Range(
            room.x.min + d.problem_size, room.x.max + d.problem_size
        )


class TestActionsN:
    def test_stretch(self):
        ea = ExecuteAction(NS_doms, ActionType.STRETCH)
        d = ea.details
        assert ea.modified_domain.y == Range(
            ea.node.y.min - d.problem_size, ea.node.y.max
        )

    def test_squeeze(self):
        ea = ExecuteAction(NS_doms, ActionType.SQUEEZE)
        d = ea.details
        assert ea.modified_domain.y == Range(
            ea.node.y.min + d.problem_size, ea.node.y.max
        )


SN_doms = CurrentDomains(hole_ns, room_ns)


class TestActionsS:
    def test_stretch(self):
        ea = ExecuteAction(SN_doms, ActionType.STRETCH)
        d = ea.details
        assert ea.modified_domain.y == Range(
            ea.node.y.min, ea.node.y.max + d.problem_size
        )

    def test_squeeze(self):
        ea = ExecuteAction(SN_doms, ActionType.SQUEEZE)
        d = ea.details
        assert ea.modified_domain.y == Range(
            ea.node.y.min, ea.node.y.max - d.problem_size
        )
