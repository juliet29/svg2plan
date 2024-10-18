from rich import print as rprint
from actions.selection import FixLayout
from actions.leveler import level_sides
from interactive.helpers import CaseNameInput, get_layout, write_plan
from helpers.save import create_plan
from visuals.plotter import plot_general

def show_remaining(a, a1):
    def str_split(arr):
        return set(str(arr).split())
    l = str_split(a)
    l1 = str_split(a1)
    diff = l.difference(l1)
    res =  sorted([int(i) for i in diff])
    print(' '.join(map(str, res)) )


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
