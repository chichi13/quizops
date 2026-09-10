"""Provoque une panne connue et réversible dans QuizOps.

Usage : uv run outils/panne.py N
Retour à la normale : git checkout -- .

1 : virgule en trop dans data/questions.json (le serveur ne démarre plus)
2 : import d'un module qui n'existe pas dans app/main.py (le serveur ne démarre plus)
3 : le score ne compte que les questions répondues (5 justes sur 10 posées donnent 100)
4 : la colonne pseudo est renommée dans l'insertion SQLite (500 à la fin d'une partie)
"""

import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent

PANNES = {
    1: (
        "data/questions.json",
        '"reponse": 0\n  },',
        '"reponse": 0,\n  },',
    ),
    2: (
        "app/main.py",
        "from app import database, donnees, quiz",
        "from app import database, donnee, quiz",
    ),
    3: (
        "app/quiz.py",
        "    total = len(reponses)",
        '    total = len([r for r in reponses if r.get("choix") is not None])',
    ),
    4: (
        "app/database.py",
        "INSERT INTO scores (pseudo, score)",
        "INSERT INTO scores (joueur, score)",
    ),
}


def appliquer(numero: int) -> None:
    fichier, avant, apres = PANNES[numero]
    chemin = RACINE / fichier
    contenu = chemin.read_text(encoding="utf-8")
    if avant not in contenu:
        sys.exit(
            f"Panne {numero} : le motif attendu n'est pas dans {fichier} (déjà appliquée ?)"
        )
    chemin.write_text(contenu.replace(avant, apres, 1), encoding="utf-8")
    print(
        f"Panne {numero} appliquée dans {fichier}. Retour à la normale : git checkout -- {fichier}"
    )


if __name__ == "__main__":
    if (
        len(sys.argv) != 2
        or not sys.argv[1].isdigit()
        or int(sys.argv[1]) not in PANNES
    ):
        sys.exit(__doc__)
    appliquer(int(sys.argv[1]))
