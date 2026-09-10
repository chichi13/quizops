"""Vérifie data/questions.json : champs, propositions, réponses et identifiants uniques.

Usage, depuis la racine du projet : uv run python <dossier du skill>/verifier.py
Sortie : "N questions, M erreurs" ; code de retour 1 s'il y a au moins une erreur.
"""

import json
import sys
from pathlib import Path

CHEMIN = Path("data/questions.json")
CATEGORIES = {"docker", "kubernetes"}
CHAMPS = ("id", "categorie", "question", "propositions", "reponse")


def verifier(questions: list[dict]) -> list[str]:
    erreurs = []
    identifiants: set[int] = set()
    for question in questions:
        identifiant = question.get("id", "?")
        for champ in CHAMPS:
            if champ not in question:
                erreurs.append(f"question {identifiant} : champ '{champ}' manquant")
        if identifiant in identifiants:
            erreurs.append(f"question {identifiant} : identifiant en double")
        identifiants.add(identifiant)
        if question.get("categorie") not in CATEGORIES:
            erreurs.append(
                f"question {identifiant} : catégorie inconnue {question.get('categorie')!r}"
            )
        propositions = question.get("propositions", [])
        if len(propositions) != 4:
            erreurs.append(
                f"question {identifiant} : {len(propositions)} propositions au lieu de 4"
            )
        if question.get("reponse") not in (0, 1, 2, 3):
            erreurs.append(
                f"question {identifiant} : réponse {question.get('reponse')!r} hors de 0 à 3"
            )
        if not str(question.get("question", "")).strip().endswith("?"):
            erreurs.append(
                f"question {identifiant} : l'énoncé ne se termine pas par un point d'interrogation"
            )
    return erreurs


if __name__ == "__main__":
    try:
        contenu = json.loads(CHEMIN.read_text(encoding="utf-8"))
    except json.JSONDecodeError as erreur:
        sys.exit(f"JSON invalide : {erreur}")
    problemes = verifier(contenu)
    for probleme in problemes:
        print(f"- {probleme}")
    print(
        f"{len(contenu)} questions, {len(problemes)} erreur{'s' if len(problemes) > 1 else ''}"
    )
    sys.exit(1 if problemes else 0)
