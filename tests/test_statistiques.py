"""Statistiques globales : nombre de parties et score moyen."""

from fastapi.testclient import TestClient

from app.main import app
from tests.outils import reponses_fausses, reponses_justes

client = TestClient(app)


def test_les_statistiques_ont_un_nombre_de_parties_et_une_moyenne():
    statistiques = client.get("/api/statistiques").json()
    assert set(statistiques) >= {"nb_parties", "moyenne"}


def test_deux_parties_font_monter_le_compteur_de_deux():
    avant = client.get("/api/statistiques").json()["nb_parties"]
    questions = client.get("/api/questions").json()
    client.post(
        "/api/answers", json={"pseudo": "hugo", "reponses": reponses_justes(questions)}
    )
    client.post(
        "/api/answers", json={"pseudo": "hugo", "reponses": reponses_fausses(questions)}
    )
    assert client.get("/api/statistiques").json()["nb_parties"] == avant + 2
