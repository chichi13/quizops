"""Fonctions partagées par les tests."""

import json
from pathlib import Path

CHEMIN_QUESTIONS = Path(__file__).resolve().parent.parent / "data" / "questions.json"


def questions_avec_reponses() -> dict[int, dict]:
    """Les questions du fichier de données, indexées par identifiant, avec la bonne réponse."""
    with open(CHEMIN_QUESTIONS, encoding="utf-8") as fichier:
        return {question["id"]: question for question in json.load(fichier)}


def reponses_justes(questions: list[dict]) -> list[dict]:
    """Une réponse juste pour chaque question posée."""
    corrige = questions_avec_reponses()
    return [
        {"question_id": q["id"], "choix": corrige[q["id"]]["reponse"]}
        for q in questions
    ]


def reponses_fausses(questions: list[dict]) -> list[dict]:
    """Une réponse fausse pour chaque question posée."""
    corrige = questions_avec_reponses()
    return [
        {"question_id": q["id"], "choix": (corrige[q["id"]]["reponse"] + 1) % 4}
        for q in questions
    ]
