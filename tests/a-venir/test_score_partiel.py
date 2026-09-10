"""Le score compte les questions posées, pas seulement celles qui ont reçu une réponse."""

from fastapi.testclient import TestClient

from app.main import app
from tests.outils import reponses_justes

client = TestClient(app)


def test_cinq_bonnes_reponses_sur_dix_questions_donnent_cinquante():
    questions = client.get("/api/questions").json()
    reponses = reponses_justes(questions)
    for reponse in reponses[5:]:
        reponse["choix"] = None
    partie = {"pseudo": "fanny", "reponses": reponses}
    assert client.post("/api/answers", json=partie).json()["score"] == 50
