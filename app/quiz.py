"""Tirage des questions et calcul du score."""

import random

NOMBRE_QUESTIONS_PAR_PARTIE = 10


def tirer_questions(
    questions: list[dict], nombre: int = NOMBRE_QUESTIONS_PAR_PARTIE
) -> list[dict]:
    """Tire au hasard les questions d'une partie, sans doublon."""
    return random.sample(questions, min(nombre, len(questions)))


def sans_reponse(question: dict) -> dict:
    """Copie de la question sans la bonne réponse, pour l'envoyer au navigateur."""
    return {cle: valeur for cle, valeur in question.items() if cle != "reponse"}


def compter_bonnes_reponses(
    reponses: list[dict], questions_par_id: dict[int, dict]
) -> int:
    """Compte les réponses dont le choix correspond à la bonne réponse."""
    bonnes = 0
    for reponse in reponses:
        question = questions_par_id.get(reponse["question_id"])
        if question is not None and reponse.get("choix") == question["reponse"]:
            bonnes += 1
    return bonnes


def calculer_score(reponses: list[dict], questions_par_id: dict[int, dict]) -> int:
    """Score de la partie, en pourcentage de bonnes réponses."""
    repondues = [reponse for reponse in reponses if reponse.get("choix") is not None]
    bonnes = compter_bonnes_reponses(repondues, questions_par_id)
    return round(bonnes / len(repondues) * 100)


def filtrer_par_categorie(questions: list[dict], categorie: str | None) -> list[dict]:
    """Les questions d'une catégorie, ou toutes les questions si aucune n'est demandée."""
    if categorie is None:
        return questions
    return [question for question in questions if question["categorie"] == categorie]
