import time
from beaupy import confirm, prompt, select, select_multiple
from beaupy.spinners import *
from rich.console import Console

console = Console()

# Confirm a dialog
if confirm("Will you take the ring to Mordor?"):
    names = [
        "Frodo Baggins",
        "Samwise Gamgee",
        "Legolas",
        "Aragorn",
        "[red]Sauron[/red]",
    ]
    console.print("Who are you?")
    # Choose one item from a list
    name = select(names, cursor="🢧", cursor_style="cyan")
    console.print(f"Alámenë, {name}")


    item_options = [
        "The One Ring",
        "Dagger",
        "Po-tae-toes",
        "Lightsaber (Wrong franchise! Nevermind, roll with it!)",
    ]
    console.print("What do you bring with you?")
    # Choose multiple options from a list
    items = select_multiple(item_options, tick_character='🎒', ticked_indices=[0], maximal_count=3)