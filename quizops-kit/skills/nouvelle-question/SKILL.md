---
name: nouvelle-question
description: Ajoute une question au quiz QuizOps dans data/questions.json puis vérifie le fichier. À utiliser quand on demande d'ajouter, de créer ou d'insérer une question de quiz.
argument-hint: "[énoncé de la question]"
allowed-tools: Read, Edit, Bash(uv run python *)
---
Ajoute une question au quiz QuizOps.

1. Lis `data/questions.json` et repère le plus grand `id`.
2. Rédige la question à partir de la demande : $ARGUMENTS. Si la catégorie n'est pas évidente, demande-la (`docker` ou `kubernetes`). Quatre propositions plausibles, une seule juste ; `reponse` est l'index de la bonne réponse, de 0 à 3. Suis le gabarit `modele.json` de ce dossier.
3. Ajoute l'objet à la fin du tableau, avec `id` égal au plus grand id plus un.
4. Lance `uv run python ${CLAUDE_SKILL_DIR}/verifier.py` et corrige jusqu'à obtenir `0 erreur`.
5. Affiche la question ajoutée et le résultat de la vérification. Ne committe pas.
