import string
import sys
sys.path.append("/Users/julietnwagwuume-ezeoke/_UILCode/gqe-phd/svg2plan/_scripts")

import os 
from typing_extensions import Annotated
from placement2.attract import adjust_domains
from read.svg_reader import SVGReader
import networkx as nx
import json
import typer
from rich import print as rprint
from rich.prompt import Confirm, Prompt

SVG_PATHS =  "/Users/julietnwagwuume-ezeoke/_UILCode/gqe-phd/svg2plan/svg_imports"

JSON_PATH = "test.json"

def complete_case(incomplete: str):
    case_names = os.listdir(SVG_PATHS)
    for name in os.listdir(SVG_PATHS):
        if name.startswith(incomplete):
            yield (name)
        else:
            return tuple(case_names)

def stringify(ix, e):
    u,v = e
    return f"{ix}. {u} - {v}"


def is_window_edge(e: tuple[str, str]):
    return False

def assign_details(connections: list[tuple[str, str]]):
    # TODO make dict type... 
    with open(JSON_PATH, "r") as file:
        details = json.load(file)

    window_types = details["WINDOWS"]
    door_types = details["DOORS"]
    window_ids = [str(i["id"]) for i in window_types]
    door_ids = [str(i["id"]) for i in door_types]

    responses = []
    for ix, e in enumerate(connections):
        if is_window_edge(e):
            r = Prompt.ask(stringify(ix, e), choices = window_ids)
            stype = "WINDOW"
        else:
            r = Prompt.ask(stringify(ix, e), choices = door_ids)
            stype = "DOOR"
        responses.append((e, stype, r))
    rprint("assigned edges", responses)
    return responses

def assess_edges(G: nx.DiGraph):
    n_edges = len(list(G.edges))
    rprint(f"Number of edges to assess: {n_edges}")
    responses = []
    for  ix, e in enumerate(G.edges):
        responses.append(Confirm.ask(stringify(ix+1, e))) 
    
    valid_edges = [list(G.edges)[ix] for ix, val in enumerate(responses) if val]
    rprint("valid_edges:", valid_edges)
    return valid_edges

def handle_edges(G: nx.DiGraph):
    valid_edges = assess_edges(G)
    rprint("**** Beginning to assign edges ****")
    return assign_details(valid_edges)

    



app = typer.Typer(no_args_is_help=True)

@app.command()
def read_svg(case_name: Annotated[str, typer.Argument(help="case_name", autocompletion=complete_case)]):
    rprint(f"Reading {case_name}")
    sv = SVGReader(case_name)
    sv.run()
    domains, [Gx, Gy] = adjust_domains(sv.layout.domains)

    rprint("\n ---- Beginning to assess X edges -----")
    x_edges = handle_edges(Gx)

    rprint("\n ---- Beginning to assess Y edges -----")
    y_edges = handle_edges(Gy)

    # TODO: write to connectivity graph, pass graph to leveler.. 


    




    



if __name__ == "__main__":
    app()