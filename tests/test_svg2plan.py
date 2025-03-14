import math

import pytest
import shapely

from svg2plan.actions.leveler import level_sides
from svg2plan.actions.selection import FixLayout
from svg2plan.constants import BASE_PATH
from svg2plan.helpers.shapely import domain_to_shape
from svg2plan.placement.attract import adjust_domains

# from svg2plan.placement.cardinal import create_cardinal_dags
from svg2plan.svg_reader import SVGReader


def run_svg(path):
    sv = SVGReader(BASE_PATH /path)
    sv.run()
    ad_layout = adjust_domains(sv.domains)
    # Gxc, Gyc = create_cardinal_dags(ad_layout)
    fl = FixLayout(ad_layout)
    fl.run_to_completion()
    return level_sides(fl.bl.layout)


path_parameters = "path", [
    "svg_imports/bol_5.svg",
    "svg_imports/red_d3.svg",
    "svg_imports/amb_b1.svg",
    "tests/svgs/_05_rect.svg",
    # "tests/svgs/messy.svg",
]


@pytest.mark.parametrize(*path_parameters)
def test_domains_are_valid_and_rectangular(path):
    domains = run_svg(path)
    union_res = shapely.unary_union([domain_to_shape(i) for i in domains.values()]) 

    assert shapely.is_valid(union_res), shapely.is_valid_reason(union_res)

    assert shapely.get_num_interior_rings(union_res) == 0

    concave_hull_ext = shapely.get_exterior_ring(shapely.concave_hull(union_res))
    union_ext = shapely.get_exterior_ring(union_res)
    assert union_ext and concave_hull_ext
    assert set(union_ext.coords) == set(concave_hull_ext.coords)

    assert math.isclose(union_res.minimum_rotated_rectangle.area, union_res.area)





# TODO also troubleshoot the process of adding adjacencies using Gxc, Gyc in svg2pla/interactive..
