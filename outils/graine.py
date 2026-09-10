"""Remplit la base avec douze scores connus, pour les TP qui ont besoin de données.

Usage : uv run outils/graine.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app import database

SCORES = [
    ("alice", 90),
    ("bob", 70),
    ("carole", 100),
    ("dan", 40),
    ("emma", 80),
    ("fanny", 60),
    ("gilles", 50),
    ("hugo", 30),
    ("iris", 90),
    ("julie", 20),
    ("karim", 70),
    ("lea", 80),
]

if __name__ == "__main__":
    database.initialiser()
    for pseudo, score in SCORES:
        database.enregistrer_score(pseudo, score)
    print(f"{len(SCORES)} scores insérés")
