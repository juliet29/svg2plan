# from svg2plan.actions.leveler import level_sides
# from svg2plan.actions.selection import FixLayout
# from svg2plan.constants import BASE_PATH
# from svg2plan.placement.attract import adjust_domains
# from svg2plan.placement.cardinal import create_cardinal_dags
# from svg2plan.svg_reader import SVGReader
# import pytest


# @pytest.skip(reason="Not testsed all the way through.. ")
# def test_svg2_plan():
#     sv = SVGReader(BASE_PATH / "svg_imports" / "red_b1.svg")
#     sv.run()
#     ad_layout = adjust_domains(sv.domains)
#     # Gxc, Gyc = create_cardinal_dags(ad_layout)
#     fl = FixLayout(ad_layout)
#     fl.run_to_completion()
#     new_doms = level_sides(fl.bl.layout)
#     assert new_doms


# TODO also troubleshoot the process of adding adjacencies using Gxc, Gyc in svg2pla/interactive.. 