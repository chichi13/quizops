"""Défi A : le chronomètre. Une partie peut envoyer sa durée, le classement l'affiche."""

from fastapi.testclient import TestClient

from app.main import app
from tests.outils import reponses_justes

client = TestClient(app)


def jouer(pseudo: str, duree: int) -> dict:
    questions = client.get("/api/questions").json()
    partie = {
        "pseudo": pseudo,
        "reponses": reponses_justes(questions),
        "duree_secondes": duree,
    }
    return client.post("/api/answers", json=partie).json()


def test_la_duree_est_renvoyee_avec_le_score():
    assert jouer("iris", 42)["duree_secondes"] == 42


def test_une_partie_sans_duree_reste_acceptee():
    questions = client.get("/api/questions").json()
    partie = {"pseudo": "iris", "reponses": reponses_justes(questions)}
    assert client.post("/api/answers", json=partie).status_code == 200


def test_a_score_egal_la_partie_la_plus_rapide_est_devant():
    jouer("lent", 90)
    jouer("rapide", 30)
    classement = client.get("/api/scores").json()
    positions = {entree["pseudo"]: rang for rang, entree in enumerate(classement)}
    assert positions["rapide"] < positions["lent"]
