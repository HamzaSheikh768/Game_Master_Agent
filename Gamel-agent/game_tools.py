from agents import function_tool
import random

@function_tool
def roll_dice() -> str:
    return f"You rolled a {random.randint(1, 8)}!"

@function_tool
def generate_event() -> str:
    events = [
        "You met a mysterious wizard",
        "You fell into a trap"
    ]
    return random.choice(events)    