"""Tests de l'API de QuizOps."""

import sqlite3

from fastapi.testclient import TestClient

from app import database
from app.main import app
from tests.outils import reponses_fausses, reponses_justes

client = TestClient(app)


def test_la_page_d_accueil_repond():
    assert client.get("/").status_code == 200


def test_les_fichiers_statiques_sont_servis():
    assert client.get("/static/app.js").status_code == 200


def test_une_partie_contient_dix_questions():
    questions = client.get("/api/questions").json()
    assert len(questions) == 10


def test_les_questions_ne_contiennent_pas_la_reponse():
    for question in client.get("/api/questions").json():
        assert "reponse" not in question


def test_chaque_question_a_quatre_propositions():
    for question in client.get("/api/questions").json():
        assert len(question["propositions"]) == 4


def test_les_identifiants_sont_uniques():
    identifiants = [question["id"] for question in client.get("/api/questions").json()]
    assert len(identifiants) == len(set(identifiants))


def test_toutes_bonnes_reponses_donnent_cent():
    questions = client.get("/api/questions").json()
    partie = {"pseudo": "alice", "reponses": reponses_justes(questions)}
    assert client.post("/api/answers", json=partie).json()["score"] == 100


def test_toutes_mauvaises_reponses_donnent_zero():
    questions = client.get("/api/questions").json()
    partie = {"pseudo": "bob", "reponses": reponses_fausses(questions)}
    assert client.post("/api/answers", json=partie).json()["score"] == 0


def test_la_reponse_reprend_le_pseudo():
    questions = client.get("/api/questions").json()
    partie = {"pseudo": "carole", "reponses": reponses_justes(questions)}
    assert client.post("/api/answers", json=partie).json()["pseudo"] == "carole"


def test_le_score_est_enregistre_en_base():
    def nombre_de_scores() -> int:
        with sqlite3.connect(database.chemin_base()) as base:
            return base.execute("SELECT COUNT(*) FROM scores").fetchone()[0]

    avant = nombre_de_scores()
    questions = client.get("/api/questions").json()
    client.post(
        "/api/answers", json={"pseudo": "dan", "reponses": reponses_justes(questions)}
    )
    assert nombre_de_scores() == avant + 1
