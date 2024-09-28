from dataclasses import dataclass
from typing import Dict
from domains.domain import Domain
from fixes.id_helpers import get_domain_directions, get_problem_size
from fixes.interfaces import SIDEHOLE_ACTIONS, ActionDetails, Problem, ProblemType
from helpers.layout import Layout
from helpers.directions import Direction
from fixes.interfaces import LayoutBase
from shapely import Polygon, union_all, STRtree, LinearRing
from helpers.helpers import key_from_value, compare_sequences
from helpers.shapely import shape_to_domain


def find_holes(shapes: list[Polygon]):
    union = union_all(shapes)
    assert isinstance(union, Polygon)
    return [Polygon(h) for h in union.interiors if isinstance(h, LinearRing)]

def find_rooms_surrounding_hole(hole: Polygon, tree: STRtree, shapes: Dict[str, Polygon]) -> list[str]:
    indices = tree.query_nearest(hole)
    nearest = tree.geometries.take(indices).tolist()
    rooms = [key_from_value(shapes, p) for p in nearest]
    return rooms


def create_action_for_problem(rooms_and_hole: tuple[list[str], Domain], domains: Dict[str, Domain]):
    rooms, hole_domain  = rooms_and_hole
    room_domains = [domains[r] for r in rooms]

    def create_action_details_for_room(room: Domain):
        cmp = get_domain_directions(room, hole_domain, consider_overlap=False)
        drns = cmp.get_domain_directions(room)
        try:
            [drn] = drns
        except:
            raise Exception("Domain should only have one relationship to hole.. ")
        return ActionDetails(room, drn, get_problem_size(hole_domain, drn), SIDEHOLE_ACTIONS)
    
    return [create_action_details_for_room(i) for i in room_domains]
       

def create_hole_problems(layout: Layout):
    shape_list = list(layout.shapes.values())
    tree = STRtree(shape_list)
    holes = find_holes(shape_list)
    room_lists = [find_rooms_surrounding_hole(h, tree, layout.shapes) for h in holes]
    problems: list[Problem] = []
    for ix, (rooms, hole) in enumerate(zip(room_lists, holes)):
        hole_domain = shape_to_domain(hole) 
        p = Problem(ix, ProblemType.HOLE, rooms, hole_domain)
        p.action_details.extend(create_action_for_problem((rooms, hole_domain), layout.domains))
        problems.append(p)
    return problems

    


