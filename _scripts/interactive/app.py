from pathlib import Path
import sys

sys.path.append(str(Path.cwd().parent))

import typer
from interactive.subsurfaces import create_window, create_door
from interactive.init import init
from interactive.edges import (
    show_edges,
    show_subsurfaces,
    assign_connectivity,
    assign_subsurfaces,
    save_connectivity_graph,
)


app = typer.Typer(no_args_is_help=True, pretty_exceptions_show_locals=False)

app.command()(init)
app.command()(create_window)
app.command()(create_door)

app.command()(show_edges)
app.command()(show_subsurfaces)
app.command()(assign_connectivity)
app.command()(assign_subsurfaces)
app.command()(save_connectivity_graph)


@app.callback()
def main(ctx: typer.Context):
    pass


if __name__ == "__main__":
    app()
