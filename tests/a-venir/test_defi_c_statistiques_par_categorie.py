"""Défi C : le détail du score par catégorie."""

from fastapi.testclient import TestClient

from app.main import app
from tests.outils import reponses_justes

client = TestClient(app)


def jouer_parfait() -> dict:
    questions = client.get("/api/questions").json()
    partie = {"pseudo": "karim", "reponses": reponses_justes(questions)}
    return client.post("/api/answers", json=partie).json()


def test_le_resultat_detaille_le_score_par_categorie():
    resultat = jouer_parfait()
    assert set(resultat["par_categorie"]) == {"docker", "kubernetes"}


def test_chaque_categorie_compte_les_bonnes_reponses_et_le_total():
    for detail in jouer_parfait()["par_categorie"].values():
        assert detail["bonnes"] == detail["total"]


def test_la_somme_des_totaux_est_le_nombre_de_questions_posees():
    resultat = jouer_parfait()
    assert sum(detail["total"] for detail in resultat["par_categorie"].values()) == 10
