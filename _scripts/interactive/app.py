from pathlib import Path
import sys

sys.path.append(str(Path.cwd().parent))

import typer
from interactive.subsurfaces import (
    copy_existing_subsurfaces,
    create_window,
    create_door,
)
from interactive.init import init
from interactive.edges import (
    assign_remaining_subsurfaces,
    show_edges,
    show_subsurfaces,
    save_connectivity_graph,
)
from interactive.finish import clean_up_domains
from interactive.prompt_edges import assign_connectivity, assign_subsurfaces, reset_edge_details


app = typer.Typer(no_args_is_help=True, pretty_exceptions_show_locals=False)

app.command()(init)

app.command()(create_window)
app.command()(create_door)
app.command()(copy_existing_subsurfaces)

app.command()(assign_connectivity)
app.command()(assign_subsurfaces)
app.command()(reset_edge_details)

app.command()(show_edges)
app.command()(show_subsurfaces)
app.command()(save_connectivity_graph)
app.command()(assign_remaining_subsurfaces)

app.command()(clean_up_domains)


@app.callback()
def main(ctx: typer.Context):
    pass


if __name__ == "__main__":
    app()
