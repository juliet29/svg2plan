from pathlib import Path
import sys
sys.path.append(str(Path.cwd().parent))

import shutil
import json
from typing_extensions import Annotated
from decimal import Decimal

import typer
from rich import print as rprint
import networkx as nx

from read.svg_reader import SVGReader
from placement2.attract import adjust_domains
from domains.domain import create_json_doman_dict
from placement2.connectivity import create_cardinal_dags
from export.saver import read_pickle, write_pickle


## use pathlib
## pass in svg, dimensions info
## create folder with svg name, appending dimension info?
## make a copy of the svg in that folder
## create and save domains using dimensions info
## ---
## create and save graphs
## in seperate file / command read domains and graph => need to unify context..

ROOT_DIR = Path.cwd().parent.parent
OUTPUT_DIR = ROOT_DIR / "outputs2"
SVG_DIR = ROOT_DIR / "svg_imports"


def complete_case(incomplete: str):
    case_names = [i.name for i in SVG_DIR.glob("*.svg")]
    for name in case_names:
        if name.startswith(incomplete):
            yield (name)
        else:
            return tuple(case_names)
        
def adj_graph_to_json(G):
    res = nx.node_link_data(G)
    for link in res["links"]:
        link["size"] = str(link["size"])
    return res

def json_to_adj_graph(G):
    Gr = nx.node_link_graph(G)
    for data in Gr.edges(data=True):
        *_, size = data
        size["size"] = Decimal(size["size"] )

    return Gr



app = typer.Typer(no_args_is_help=True)

# pixel_length: int, true_length: tuple[str, str, str]
#  Annotated[str, typer.Argument   (help="case_name", autocompletion=complete_case)]


@app.command()
def read_svg(case_name: Annotated[
        str, typer.Argument(help="case_name", autocompletion=complete_case)
    ]
):
    case_path = SVG_DIR / case_name
    output_path = OUTPUT_DIR / f"case_{case_path.stem}"

    try:
        output_path.mkdir()
        shutil.copy(case_path, output_path / case_name)
    except FileExistsError:
        print("Folder already initialized")

    sv = SVGReader(case_name)  # TODO pass dimensions..
    sv.run()
    domains, graphs = adjust_domains(sv.layout.domains)

    with (output_path / "domains.json").open("w", encoding="UTF-8") as target:
            json.dump(create_json_doman_dict(domains), target)


    write_pickle(obj=graphs, path=(output_path / "adj_graphs.pkl"))

    # json_graphs = [adj_graph_to_json(i) for i in graphs]
    # with (output_path / "adj_graphs.json").open("w", encoding="UTF-8") as target:
    #     json.dump(json_graphs, target)

    rprint(f"Saved files in '{output_path}'")

    
@app.command()
def assign_edges(case_name: Annotated[
        str, typer.Argument(help="case_name", autocompletion=complete_case)]):
    
    case_path = SVG_DIR / case_name
    output_path = OUTPUT_DIR / f"case_{case_path.stem}"
    print(output_path)

    # try:
    Gx, Gy = read_pickle(path=(output_path / "adj_graphs.pkl"))
    # except:
    #     rprint("reading graphs failed. make sure have 'read-svg'.")

    # rprint(Gx.nodes)
    
    # with (output_path / "adj_graphs.json").open("w",        encoding="UTF-8") as target:
    # # TODO how does it know which folder? has to be passed in aslo.. 
    #     pass


# @app.command()
# def assign_edges():
#     ctx.obj.process(lambda data: data["graph"])
#     print(ctx.obj)
#     try:
#         Gx, Gy = ctx.obj["graphs"]
#         Gxd, Gyd = create_cardinal_dags(Gx, Gy)
#     except TypeError:
#         print("need to 'read_svg' before can assign edges")

    
    



@app.callback()
def main(ctx: typer.Context):
    pass

if __name__ == "__main__":
    app()
