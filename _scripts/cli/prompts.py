import typer
from rich.prompt import Prompt, Confirm
edges = [("bath", "kitchen"), ("living", "dining"), ("m_bed", "bath"), ("living", "closet")]

def stringify(e):
    u,v = e
    return f"{u} - {v}"

def main():
    # name = Prompt.ask("Enter your name :sunglasses:")
    # print(f"Hey there {name}!")
    responses = []
    for e in edges:
        responses.append(Confirm.ask(stringify(e)))
    
    valid_eges = [edges[ix] for ix, val in enumerate(responses) if val]
    print("valid_edges:", valid_eges)
    return

if __name__ == "__main__":
    typer.run(main)