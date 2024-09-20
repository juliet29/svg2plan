import pytest
from new_corners.range import nonDecimalRange, Range
from new_corners.domain import Domain
from actions.actions import ExecuteAction
from actions.interfaces import Action
from actions.details import Details
from svg_helpers.directions import Direction
from actions.interfaces import CurrentDomains


a_x = nonDecimalRange(10, 20).toRange()
b_x = nonDecimalRange(20, 25).toRange()
y = nonDecimalRange(10, 30).toRange()

room = Domain(name="room", x=a_x, y=y)
hole = Domain(name="hole", x=b_x, y=y)
curr_doms = CurrentDomains(room, hole)


d = Details(curr_doms)
d.run()


def test_relative_direction():
    assert d.relative_direction == Direction.WEST


def test_problem_size():
    assert d.problem_size == b_x.size

def test_stretch():
    ea = ExecuteAction(curr_doms, Action.STRETCH)
    assert ea.modified_domain.x == Range(room.x.min, room.x.max + d.problem_size)


def test_squeeze():
    ea = ExecuteAction(curr_doms, Action.SQUEEZE)
    assert ea.modified_domain.x == Range(room.x.min, room.x.max - d.problem_size)

def test_push():
    ea = ExecuteAction(curr_doms, Action.PUSH)
    assert ea.modified_domain.x == Range(room.x.min - d.problem_size, room.x.max - d.problem_size)

def test_pull():
    ea = ExecuteAction(curr_doms, Action.PULL)
    assert ea.modified_domain.x == Range(room.x.min + d.problem_size, room.x.max + d.problem_size)
