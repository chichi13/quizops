#!/usr/bin/env bash
# Reproduit l'erreur classique : un fichier .env avec une clé est committé par mégarde.
# Usage : outils/fuite.sh
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"

printf 'ANTHROPIC_API_KEY=sk-ant-%s\n' 'fausse-cle-0000' > .env
git add -f .env
git commit -q -m "Ajoute la configuration locale"
echo "Le fichier .env est committé avec une fausse clé. À vous de jouer."
