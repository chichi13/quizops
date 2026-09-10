---
description: Relit les modifications non committées avec la grille du projet et classe les constats par gravité.
disable-model-invocation: true
---
Relis les modifications non committées : `git diff` puis `git diff --staged`.

Pour chaque fichier modifié, réponds aux six questions de la grille :

1. Fait-il ce qui a été demandé ?
2. Fait-il autre chose (fichier créé en plus, dépendance ajoutée, fonction renommée) ?
3. Que se passe-t-il aux bords : liste vide, `None`, zéro, entrée invalide ?
4. Les erreurs sont-elles traitées ou avalées ?
5. Y a-t-il un risque de sécurité : entrée non validée, secret en dur, SQL assemblé ?
6. Est-ce maintenable dans six mois : noms explicites, fonctions courtes, cohérence avec le reste ?

Rends un tableau `constat | fichier:ligne | gravité` avec trois gravités : bloquant, à corriger, remarque.
Ne modifie aucun fichier.
