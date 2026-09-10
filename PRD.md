# QuizOps : cahier des charges

## Objectif

Proposer un quiz de dix questions sur Docker et Kubernetes, jouable dans un navigateur, qui enregistre le score de chaque partie. L'application sert de terrain d'entraînement à la formation Vibe Coding : elle doit rester lisible par quelqu'un qui ne connaît pas Python.

## Utilisateurs

- Un apprenant qui révise Docker ou Kubernetes et veut se tester en cinq minutes.
- Un formateur qui consulte les scores pour repérer les notions mal comprises.

## Fonctionnalités existantes

- Une partie tire dix questions au hasard parmi celles du fichier `data/questions.json`.
- Chaque question propose quatre réponses ; l'apprenant peut passer une question.
- À la fin de la partie, le score en pourcentage est affiché et enregistré avec le pseudo.

## Hors périmètre

- Pas de compte utilisateur, pas d'authentification.
- Pas d'édition des questions depuis l'interface : le fichier JSON est la seule source.
- Pas de minuteur ni de mode multijoueur dans cette version.

## Contraintes techniques

- Python 3.13, FastAPI et Uvicorn, base SQLite dans `quizops.db` (jamais versionnée).
- Interface en HTML, CSS et JavaScript natifs, sans framework ni dépendance.
- Environnement géré par `uv` ; qualité vérifiée par `ruff` et `pytest`.
- Les modules ont des noms imposés : `app/main.py`, `app/quiz.py`, `app/donnees.py`, `app/database.py`.

## Modèle de données

- Une question : `id` (entier unique), `categorie` (`docker` ou `kubernetes`), `question`, `propositions` (quatre chaînes), `reponse` (index de 0 à 3).
- Un score : `pseudo` (1 à 30 caractères), `score` (entier de 0 à 100), `date` (horodatage SQLite).
- Une partie envoyée par le navigateur : `pseudo` et la liste des `reponses`, chacune avec `question_id` et `choix` (index, ou `null` si la question a été passée).

## API

| Méthode | Route | Rôle |
|---------|-------|------|
| `GET` | `/api/questions` | Dix questions tirées au hasard, sans le champ `reponse` |
| `POST` | `/api/answers` | Reçoit les réponses d'une partie, enregistre et renvoie le score |
| `GET` | `/` et `/static/...` | L'interface |

## Critères d'acceptation

- [ ] `GET /api/questions` renvoie exactement dix questions, sans doublon et sans le champ `reponse`.
- [ ] Dix bonnes réponses donnent un score de 100 ; dix mauvaises donnent 0.
- [ ] Une partie de dix questions dont cinq seulement ont reçu une réponse, toutes justes, donne 50.
- [ ] Chaque partie terminée ajoute exactement une ligne dans la table `scores`.
- [ ] La suite `uv run pytest -q` est verte avant chaque commit.

## Lots à venir

### Lot 1 : filtrer par catégorie

`GET /api/questions?categorie=docker` ne renvoie que des questions Docker. Tests : `tests/a-venir/test_categories_lot1.py`. Contrôle : `curl -s 'http://127.0.0.1:8000/api/questions?categorie=docker' | grep -c kubernetes` renvoie `0`.

### Lot 2 : refuser une catégorie inconnue

`GET /api/questions?categorie=inconnue` renvoie un code 404, pas une liste vide. Tests : `tests/a-venir/test_categories_lot2.py`. Contrôle : `curl -s -o /dev/null -w '%{http_code}' 'http://127.0.0.1:8000/api/questions?categorie=inconnue'` renvoie `404`.

### Lot 3 : lister les catégories

`GET /api/categories` renvoie la liste triée des catégories, et l'interface propose un bouton par catégorie avant de commencer. Tests : `tests/a-venir/test_categories_lot3.py`. Contrôle : `curl -s http://127.0.0.1:8000/api/categories` renvoie `["docker","kubernetes"]`.

## Composants critiques

- **L'entrée de `POST /api/answers`** : que se passe-t-il si la liste des réponses est vide, si un identifiant de question n'existe pas, si le choix vaut 7 ou si le pseudo fait 200 caractères ? Aujourd'hui la route accepte tout : une erreur silencieuse produit un score faux, une erreur bruyante produit un 500.
- **Le chargement de `data/questions.json`** : une virgule en trop ou un champ manquant empêche le serveur de démarrer. La validation de `charger_questions` doit rester stricte et le message d'erreur doit nommer la question fautive.
- **L'écriture dans SQLite** : le score est enregistré après le calcul ; si l'insertion échoue, la partie est perdue sans que le joueur le sache. Toute modification du schéma doit être couverte par un test.
