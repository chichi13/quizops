"""Accès à la base SQLite des scores."""

import os
import sqlite3
from pathlib import Path


def chemin_base() -> Path:
    """Chemin de la base : quizops.db, ou la variable d'environnement QUIZOPS_DB."""
    return Path(os.environ.get("QUIZOPS_DB", "quizops.db"))


def connexion() -> sqlite3.Connection:
    return sqlite3.connect(chemin_base())


def initialiser() -> None:
    """Crée la table des scores si elle n'existe pas."""
    with connexion() as base:
        base.execute(
            "CREATE TABLE IF NOT EXISTS scores ("
            "id INTEGER PRIMARY KEY AUTOINCREMENT, "
            "pseudo TEXT NOT NULL, "
            "score INTEGER NOT NULL, "
            "date TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP)"
        )


def enregistrer_score(pseudo: str, score: int) -> None:
    with connexion() as base:
        base.execute(
            "INSERT INTO scores (pseudo, score) VALUES (?, ?)", (pseudo, score)
        )


def meilleurs_scores(limite: int = 10) -> list[dict]:
    """Les meilleurs scores, du plus haut au plus bas."""
    with connexion() as base:
        lignes = base.execute(
            "SELECT pseudo, score, date FROM scores ORDER BY score DESC, date ASC LIMIT ?",
            (limite,),
        ).fetchall()
    return [
        {"pseudo": pseudo, "score": score, "date": date}
        for pseudo, score, date in lignes
    ]


def statistiques() -> dict:
    """Nombre de parties jouées et score moyen, arrondi à une décimale."""
    with connexion() as base:
        nombre, moyenne = base.execute(
            "SELECT COUNT(*), AVG(score) FROM scores"
        ).fetchone()
    return {"nb_parties": nombre, "moyenne": round(moyenne or 0.0, 1)}
