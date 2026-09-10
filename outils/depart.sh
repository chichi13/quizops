#!/usr/bin/env bash
# Point de départ du TP N : remet le dépôt dans l'état tpN-depart, installe et lance les tests.
# Usage : outils/depart.sh N
set -euo pipefail

N="${1:?usage : outils/depart.sh N}"
cd "$(git rev-parse --show-toplevel)"

if [ -n "$(git status --porcelain)" ]; then
  echo "Des modifications ne sont pas committées. Committez-les, ou lancez : git stash" >&2
  exit 1
fi

git checkout -q -B "tp$N" "tp$N-depart"
uv sync -q
rm -f quizops.db
uv run pytest -q
