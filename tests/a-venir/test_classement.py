"""Classement : les meilleurs scores enregistrés."""

from fastapi.testclient import TestClient

from app.main import app
from tests.outils import reponses_justes

client = TestClient(app)


def jouer(pseudo: str) -> None:
    questions = client.get("/api/questions").json()
    client.post(
        "/api/answers", json={"pseudo": pseudo, "reponses": reponses_justes(questions)}
    )


def test_le_classement_est_une_liste():
    reponse = client.get("/api/scores")
    assert reponse.status_code == 200
    assert isinstance(reponse.json(), list)


def test_chaque_entree_a_un_pseudo_et_un_score():
    jouer("emma")
    for entree in client.get("/api/scores").json():
        assert "pseudo" in entree
        assert "score" in entree


def test_le_classement_est_trie_du_meilleur_au_moins_bon():
    scores = [entree["score"] for entree in client.get("/api/scores").json()]
    assert scores == sorted(scores, reverse=True)


def test_le_classement_est_limite_a_dix_entrees():
    for numero in range(12):
        jouer(f"joueur{numero}")
    assert len(client.get("/api/scores").json()) <= 10
