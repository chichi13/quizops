"""Défi B : l'export CSV du classement."""

from fastapi.testclient import TestClient

from app.main import app
from tests.outils import reponses_justes

client = TestClient(app)


def test_l_export_est_du_csv():
    reponse = client.get("/api/scores.csv")
    assert reponse.status_code == 200
    assert reponse.headers["content-type"].startswith("text/csv")


def test_la_premiere_ligne_est_l_en_tete():
    premiere_ligne = client.get("/api/scores.csv").text.splitlines()[0]
    assert premiere_ligne == "pseudo,score,date"


def test_chaque_score_du_classement_a_sa_ligne():
    questions = client.get("/api/questions").json()
    client.post(
        "/api/answers", json={"pseudo": "julie", "reponses": reponses_justes(questions)}
    )
    nombre_entrees = len(client.get("/api/scores").json())
    lignes = client.get("/api/scores.csv").text.strip().splitlines()
    assert len(lignes) == nombre_entrees + 1
