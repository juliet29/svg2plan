import shutil
import errno
from rich import print as rprint
import typer
from typing_extensions import Annotated
from ..actions.selection import FixLayout
from ..actions.leveler import level_sides
from .helpers import (
    SVGNameInput,
    error_print,
    get_layout,
    get_output_path,
    remove_files,
    write_plan,
)
from ..helpers.save import create_plan
from ..visuals.plotter import plot_general
from ..constants import BASE_PATH


def copyanything(src, dst):
    try:
        shutil.copytree(src, dst)
    except OSError as exc:  # python >2.5
        if exc.errno in (errno.ENOTDIR, errno.EINVAL):
            shutil.copy(src, dst)
        else:
            raise


def show_remaining(a, a1):
    def str_split(arr):
        return set(str(arr).split())

    l0 = str_split(a)
    l1 = str_split(a1)
    diff = l0.difference(l1)
    res = sorted([int(i) for i in diff])
    print(" ".join(map(str, res)))


def clean_up_domains(svg_name: SVGNameInput):
    layout = get_layout(svg_name)
    fl = FixLayout(layout)

    try:
        fl.run_to_completion()
    except Exception as e:
        error_print(e)

    new_doms = level_sides(fl.bl.layout)

    plot_general(new_doms)

    write_plan(svg_name, create_plan(new_doms))


def copy_to_plan2eplus(
    svg_name: SVGNameInput,
    reset: Annotated[bool, typer.Option(help="Overwrite existing folder")] = False,
):
    output_path = get_output_path(svg_name)
    plan2eplus_path = BASE_PATH.parent / "plan2eplus/svg2plan_outputs/"
    assert plan2eplus_path.exists()

    new_path = plan2eplus_path / output_path.name
    try:
        copyanything(output_path, new_path)
    except FileExistsError:
        if reset:
            remove_files(new_path)
            new_path.rmdir()
            copyanything(output_path, new_path)
        else:
            error_print("Folder already initialized. Add `--reset` flag to overwrite")

    rprint(f"Copied contents to `{new_path}`")
