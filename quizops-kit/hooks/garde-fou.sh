#!/usr/bin/env bash
# Hook PreToolUse sur Bash : refuse les commandes destructrices avant leur exécution.
# Reçoit sur l'entrée standard le JSON de l'appel d'outil.
# Code de retour 2 : la commande est bloquée et le message sur stderr est montré à l'agent.
# Code de retour 0 : la commande passe.

commande="$(jq -r '.tool_input.command // empty')"

bloquer() {
  echo "Commande interdite par la politique du projet : $commande" >&2
  exit 2
}

# rm récursif, sauf sous /tmp
if [[ "$commande" =~ rm[[:space:]]+-[a-zA-Z]*r[a-zA-Z]*[[:space:]]+([^[:space:]]+) ]]; then
  [[ "${BASH_REMATCH[1]}" == /tmp/* ]] || bloquer
fi

# push forcé
if [[ "$commande" =~ git[[:space:]]+push.*(--force|[[:space:]]-f([[:space:]]|$)) ]]; then
  bloquer
fi

exit 0
