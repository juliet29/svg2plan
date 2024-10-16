from rich import print as rprint
from actions.selection import FixLayout
from actions.leveler import level_sides
from interactive.helpers import CaseNameInput, get_layout, write_plan
from export.save_plan import create_plan
from visuals.plotter import plot_general


def clean_up_domains(case_name: CaseNameInput):
    layout = get_layout(case_name)
    fl = FixLayout(layout)

    try:
        fl.run_to_completion()
    except Exception as e:
        rprint(e)

    new_doms = level_sides(fl.bl.layout)

    plot_general(new_doms)

    write_plan(case_name, create_plan(new_doms))
