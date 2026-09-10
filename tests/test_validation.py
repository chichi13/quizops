"""Validation des entrées de POST /api/answers : une entrée invalide est refusée avec un 422."""

from fastapi.testclient import TestClient

from app.main import app
from tests.outils import reponses_justes

client = TestClient(app)


def partie_valide() -> dict:
    questions = client.get("/api/questions").json()
    return {"pseudo": "gilles", "reponses": reponses_justes(questions)}


def test_une_partie_valide_est_acceptee():
    assert client.post("/api/answers", json=partie_valide()).status_code == 200


def test_une_liste_de_reponses_vide_est_refusee():
    partie = {"pseudo": "gilles", "reponses": []}
    assert client.post("/api/answers", json=partie).status_code == 422


def test_un_pseudo_vide_est_refuse():
    partie = partie_valide()
    partie["pseudo"] = ""
    assert client.post("/api/answers", json=partie).status_code == 422


def test_un_pseudo_trop_long_est_refuse():
    partie = partie_valide()
    partie["pseudo"] = "x" * 31
    assert client.post("/api/answers", json=partie).status_code == 422


def test_un_identifiant_de_question_inconnu_est_refuse():
    partie = partie_valide()
    partie["reponses"][0]["question_id"] = 9999
    assert client.post("/api/answers", json=partie).status_code == 422


def test_un_choix_hors_bornes_est_refuse():
    partie = partie_valide()
    partie["reponses"][0]["choix"] = 7
    assert client.post("/api/answers", json=partie).status_code == 422


def test_un_corps_qui_n_est_pas_du_json_est_refuse():
    reponse = client.post(
        "/api/answers",
        content="pas du json",
        headers={"Content-Type": "application/json"},
    )
    assert reponse.status_code == 422
