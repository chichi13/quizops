#!/usr/bin/env bash
# Vérifie la veille que le poste est prêt pour les TP. Une ligne par outil.
# Usage : outils/preflight.sh

VERSION_CLAUDE_MINIMALE="2.1.200"
statut=0

verifier() {
  local nom="$1" commande="$2" facultatif="${3:-}"
  if command -v "$commande" >/dev/null 2>&1; then
    printf '✔ %-12s %s\n' "$nom" "$($commande --version 2>&1 | head -1)"
  elif [ -n "$facultatif" ]; then
    printf '· %-12s absent (facultatif)\n' "$nom"
  else
    printf '✘ %-12s absent\n' "$nom"
    statut=1
  fi
}

verifier "claude" claude
verifier "uv" uv
verifier "python" python3
verifier "node" node
verifier "npx" npx
verifier "git" git
verifier "jq" jq
verifier "gh" gh facultatif

if command -v claude >/dev/null 2>&1; then
  version="$(claude --version | awk '{print $1}')"
  if [ "$(printf '%s\n%s\n' "$VERSION_CLAUDE_MINIMALE" "$version" | sort -V | head -1)" != "$VERSION_CLAUDE_MINIMALE" ]; then
    printf '✘ %-12s %s est plus ancien que %s : lancez claude update\n' "claude" "$version" "$VERSION_CLAUDE_MINIMALE"
    statut=1
  fi
fi

for cache in "$HOME/Library/Caches/ms-playwright" "$HOME/.cache/ms-playwright"; do
  if ls "$cache" 2>/dev/null | grep -q '^chromium'; then
    printf '✔ %-12s %s\n' "chromium" "$cache"
    chromium=1
  fi
done
if [ -z "${chromium:-}" ]; then
  printf '✘ %-12s absent : lancez npx playwright install chromium\n' "chromium"
  statut=1
fi

exit $statut
