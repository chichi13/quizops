"""Sabote QuizOps pour vérifier que les tests protègent vraiment.

Usage : uv run outils/saboter.py N
Retour à la normale : git checkout -- app/

1 : le tirage peut renvoyer deux fois la même question
2 : le score vaut toujours 100
3 : une catégorie inconnue renvoie une liste vide au lieu d'un 404
4 : une fonction dupliquée et une comparaison de chaînes avec is (terrain de revue)
"""

import sys
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent

SABOTAGES = {
    1: (
        "app/quiz.py",
        "    return random.sample(questions, min(nombre, len(questions)))",
        "    return random.choices(questions, k=min(nombre, len(questions)))",
    ),
    2: (
        "app/quiz.py",
        "    return round(bonnes / total * 100)",
        "    return 100",
    ),
    3: (
        "app/main.py",
        '        raise HTTPException(status_code=404, detail=f"Catégorie inconnue : {categorie}")',
        "        return []",
    ),
    4: (
        "app/quiz.py",
        "def sans_reponse(question: dict) -> dict:",
        (
            "def categorie_est_docker(question: dict) -> bool:\n"
            '    return question["categorie"] is "docker"\n\n\n'
            "def categorie_docker(question: dict) -> bool:\n"
            '    if question["categorie"] == "docker":\n'
            "        return True\n"
            "    else:\n"
            "        return False\n\n\n"
            "def sans_reponse(question: dict) -> dict:"
        ),
    ),
}


def appliquer(numero: int) -> None:
    fichier, avant, apres = SABOTAGES[numero]
    chemin = RACINE / fichier
    contenu = chemin.read_text(encoding="utf-8")
    if avant not in contenu:
        sys.exit(
            f"Sabotage {numero} : le motif attendu n'est pas dans {fichier} (déjà appliqué ?)"
        )
    chemin.write_text(contenu.replace(avant, apres, 1), encoding="utf-8")
    print(
        f"Sabotage {numero} appliqué dans {fichier}. Retour à la normale : git checkout -- app/"
    )


if __name__ == "__main__":
    if (
        len(sys.argv) != 2
        or not sys.argv[1].isdigit()
        or int(sys.argv[1]) not in SABOTAGES
    ):
        sys.exit(__doc__)
    appliquer(int(sys.argv[1]))
