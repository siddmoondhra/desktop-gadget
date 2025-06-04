import random

def get_note():
    with open("notes.txt", "r") as f:
        notes = f.readlines()
    return random.choice(notes).strip()
