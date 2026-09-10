"""Lot 2 : une catégorie inconnue est une erreur, pas une liste vide."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_une_categorie_inconnue_renvoie_404():
    assert client.get("/api/questions?categorie=inconnue").status_code == 404
