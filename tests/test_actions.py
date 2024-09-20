import pytest
from new_corners.range import nonDecimalRange, Range
from new_corners.domain import Domain
from actions.actions import Pull, Push, Stretch, Shrink, Details
from svg_helpers.directions import Direction

a_x = nonDecimalRange(10,20).toRange()
b_x = nonDecimalRange(20, 25).toRange()
y = nonDecimalRange(10, 30).toRange()

room = Domain(name="room", x=a_x, y=y)
hole = Domain(name="hole", x=b_x, y=y)

d = Details(node_domain=room, problem_domain=hole)
d.get_direction_relative_to_problem()
d.get_problem_size()

def test_relative_direction():
    assert d.direction_relative_to_problem == Direction.WEST

def test_problem_size():
    assert d.problem_size == b_x.size




# def test_pull():
#     pu = Pull(node_domain=room, problem_domain=hole)
#     new_room = pu.execute_action()
#     assert new_room.x == hole.x

# def test_push():
#     pu = Push(node_domain=room, problem_domain=hole)
#     new_room = pu.execute_action()
#     assert new_room.x == Range(room.x.min - pu.dist, room.x.max - pu.dist)

# def test_stretch():
#     pu = Stretch(node_domain=room, problem_domain=hole)
#     new_room = pu.execute_action()
#     assert new_room.x == Range(room.x.min, room.x.max + pu.dist)


# def test_shrink():
#     pu = Shrink(node_domain=room, problem_domain=hole)
#     new_room = pu.execute_action()
#     assert new_room.x == Range(room.x.min, room.x.max - pu.dist,)

