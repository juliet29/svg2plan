import pytest
from new_corners.range import nonDecimalRange, Range
from new_corners.domain import Domain
from actions.actions import Pull, Push, Stretch, Shrink
from actions.details import Details
from svg_helpers.directions import Direction
from actions.interfaces import CurrentDomains


a_x = nonDecimalRange(10,20).toRange()
b_x = nonDecimalRange(20, 25).toRange()
y = nonDecimalRange(10, 30).toRange()

room = Domain(name="room", x=a_x, y=y)
hole = Domain(name="hole", x=b_x, y=y)
curr_doms = CurrentDomains(room, hole)


d = Details(curr_doms)
d.run()

def test_relative_direction():
    assert d.direction_relative_to_problem == Direction.WEST

def test_problem_size():
    assert d.problem_size == b_x.size

def test_action_direction():
    pu = Stretch(curr_doms)
    pu.get_details()
    pu.get_action_direction()
    assert pu.action_direction == Direction.EAST

def test_stretch():
    pu = Stretch(curr_doms)
    pu.get_details()
    pu.get_action_direction()
    pu.execute_action()
    assert pu.new_room_domain.x == Range(room.x.min, room.x.max + pu.details.problem_size)



# def test_pull():
#     pu = Pull(node_domain=room, problem_domain=hole)
#     new_room = pu.execute_action()
#     assert new_room.x == hole.x

# def test_push():
#     pu = Push(node_domain=room, problem_domain=hole)
#     new_room = pu.execute_action()
#     assert new_room.x == Range(room.x.min - pu.dist, room.x.max - pu.dist)



# def test_shrink():
#     pu = Shrink(node_domain=room, problem_domain=hole)
#     new_room = pu.execute_action()
#     assert new_room.x == Range(room.x.min, room.x.max - pu.dist,)

