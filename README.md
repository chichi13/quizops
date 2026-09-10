# QuizOps

Un quiz de dix questions sur Docker et Kubernetes, servi par FastAPI, avec les scores dans SQLite. C'est le projet fil rouge de la formation Vibe Coding : on y fait travailler Claude Code sur du code existant.

## Installation

Prérequis : Python 3.13 et [uv](https://docs.astral.sh/uv/).

```bash
git clone https://github.com/chichi13/quizops.git
cd quizops
uv sync
```

## Lancer l'application

```bash
uv run uvicorn app.main:app --reload
```

L'interface répond sur http://127.0.0.1:8000 et la documentation de l'API sur http://127.0.0.1:8000/docs.

## Vérifier

```bash
uvx ruff format . && uvx ruff check . && uv run pytest -q
```

La même séquence tourne dans l'intégration continue (`.github/workflows/ci.yml`) à chaque poussée.

## API

| Méthode | Route | Rôle |
|---------|-------|------|
| `GET` | `/api/questions` | Dix questions au hasard, sans les bonnes réponses ; `?categorie=docker` pour filtrer |
| `GET` | `/api/categories` | La liste des catégories |
| `POST` | `/api/answers` | Reçoit les réponses d'une partie, enregistre et renvoie le score |
| `GET` | `/api/scores` | Les dix meilleurs scores |
| `GET` | `/api/statistiques` | Le nombre de parties et le score moyen |

## Structure

- `app/main.py` : les routes et le service des fichiers statiques
- `app/quiz.py` : tirage des questions, filtrage par catégorie, calcul du score
- `app/donnees.py` : chargement et validation de `data/questions.json`
- `app/database.py` : accès SQLite (`quizops.db`, créée au premier lancement, jamais versionnée)
- `static/` : l'interface, en HTML, CSS et JavaScript natifs
- `tests/` : la suite pytest ; `tests/a-venir/` : les tests des lots pas encore livrés, ignorés par pytest
- `.claude/` : le contexte, les commandes, les skills et les hooks de Claude Code pour ce projet
- `outils/` : les scripts du formateur (point de départ, pannes, sabotages, données de test)
