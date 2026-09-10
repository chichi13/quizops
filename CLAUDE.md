# QuizOps

Quiz Docker et Kubernetes : API FastAPI, base SQLite, interface HTML, CSS et JavaScript sans framework.

## Commandes

- Lancer : `uv run uvicorn app.main:app --reload` puis http://127.0.0.1:8000
- Tests : `uv run pytest -q`
- Qualité : `uvx ruff format . && uvx ruff check .`

## Structure

- `app/main.py` : les routes `/api/...` et le service des fichiers statiques
- `app/quiz.py` : tirage des questions et calcul du score
- `app/donnees.py` : chargement et validation de `data/questions.json`
- `app/database.py` : accès SQLite (`quizops.db`, jamais versionné)
- `tests/` : la suite pytest ; `tests/a-venir/` : les tests des lots pas encore livrés, ignorés par pytest
- `outils/` : scripts du formateur, à ne pas modifier

## Conventions

- Code, commentaires, noms de tests et messages de commit en français
- Pas de module `utils.py` : chaque fonction va dans le module de son sujet
- Pas de `try/except` générique : une erreur inattendue doit remonter
- Ne modifie jamais un test existant sans le dire explicitement
- Une fonctionnalité = un commit ; lance `uv run pytest -q` avant de conclure
