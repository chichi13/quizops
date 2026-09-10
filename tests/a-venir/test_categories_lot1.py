"""Lot 1 : filtrer les questions par catégorie."""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_le_filtre_docker_ne_renvoie_que_des_questions_docker():
    questions = client.get("/api/questions?categorie=docker").json()
    assert questions, "au moins une question attendue"
    assert all(question["categorie"] == "docker" for question in questions)


def test_le_filtre_kubernetes_ne_renvoie_que_des_questions_kubernetes():
    questions = client.get("/api/questions?categorie=kubernetes").json()
    assert questions, "au moins une question attendue"
    assert all(question["categorie"] == "kubernetes" for question in questions)
