// Interface de QuizOps : une partie de dix questions, sans dépendance.

const accueil = document.getElementById("accueil");
const partie = document.getElementById("partie");
const fin = document.getElementById("fin");
const champPseudo = document.getElementById("pseudo");

let questions = [];
let index = 0;
let reponses = [];

async function demarrerPartie() {
  const reponse = await fetch("/api/questions");
  questions = await reponse.json();
  index = 0;
  reponses = [];
  accueil.hidden = true;
  fin.hidden = true;
  partie.hidden = false;
  afficherQuestion();
}

function afficherQuestion() {
  const question = questions[index];
  document.getElementById("progression").textContent =
    `Question ${index + 1} sur ${questions.length}`;
  document.getElementById("question").textContent = question.question;

  const conteneur = document.getElementById("propositions");
  conteneur.innerHTML = "";
  question.propositions.forEach((proposition, choix) => {
    const bouton = document.createElement("button");
    bouton.textContent = proposition;
    bouton.addEventListener("click", () => repondre(choix));
    conteneur.appendChild(bouton);
  });
}

function repondre(choix) {
  reponses.push({ question_id: questions[index].id, choix: choix });
  suivante();
}

function suivante() {
  index += 1;
  if (index < questions.length) {
    afficherQuestion();
  } else {
    terminerPartie();
  }
}

async function terminerPartie() {
  const pseudo = champPseudo.value.trim() || "anonyme";
  const reponse = await fetch("/api/answers", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ pseudo: pseudo, reponses: reponses }),
  });
  const resultat = await reponse.json();
  partie.hidden = true;
  fin.hidden = false;
  document.getElementById("resultat").textContent =
    `${resultat.pseudo}, votre score est de ${resultat.score} %.`;
}

document.getElementById("demarrer").addEventListener("click", demarrerPartie);
document.getElementById("passer").addEventListener("click", () => {
  reponses.push({ question_id: questions[index].id, choix: null });
  suivante();
});
document.getElementById("rejouer").addEventListener("click", () => {
  fin.hidden = true;
  accueil.hidden = false;
});
