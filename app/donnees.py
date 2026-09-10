"""Chargement des questions du quiz depuis le fichier JSON."""

import json
from pathlib import Path

CHEMIN_QUESTIONS = Path(__file__).resolve().parent.parent / "data" / "questions.json"
CHAMPS_OBLIGATOIRES = ("id", "categorie", "question", "propositions", "reponse")


def charger_questions(chemin: Path = CHEMIN_QUESTIONS) -> list[dict]:
    """Lit le fichier JSON et vérifie que chaque question a tous ses champs."""
    with open(chemin, encoding="utf-8") as fichier:
        questions = json.load(fichier)
    for question in questions:
        for champ in CHAMPS_OBLIGATOIRES:
            if champ not in question:
                identifiant = question.get("id", "?")
                raise ValueError(f"Question {identifiant} : champ '{champ}' manquant")
    return questions
