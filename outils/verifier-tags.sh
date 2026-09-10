#!/usr/bin/env bash
# Vérifie que chaque tag tpN-depart a bien le nombre de tests verts attendu.
# Usage : outils/verifier-tags.sh
set -euo pipefail
cd "$(git rev-parse --show-toplevel)"

ATTENDUS=(_ 10 10 10 14 19 29 29 31 31)  # index N = nombre de tests verts attendu au tag tpN-depart
temporaire="$(mktemp -d)"
statut=0

for numero in 1 2 3 4 5 6 7 8 9; do
  tag="tp$numero-depart"
  dossier="$temporaire/$tag"
  git worktree add "$dossier" "$tag" >/dev/null 2>&1
  verts="$(cd "$dossier" && uv sync -q && uv run pytest -q 2>/dev/null | tail -1 | grep -o '[0-9]* passed' | cut -d' ' -f1)"
  if [ "$verts" = "${ATTENDUS[$numero]}" ]; then
    printf '✔ %-11s %s passed\n' "$tag" "$verts"
  else
    printf '✘ %-11s %s passed, attendu %s\n' "$tag" "${verts:-0}" "${ATTENDUS[$numero]}"
    statut=1
  fi
  git worktree remove --force "$dossier"
done

exit $statut
