"""Lot 3 : la liste des catégories disponibles, pour les boutons de l'interface."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_la_liste_des_categories_est_triee_et_sans_doublon():
    assert client.get("/api/categories").json() == ["docker", "kubernetes"]
