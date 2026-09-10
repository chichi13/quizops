"""Tests unitaires du tirage des questions."""

from app import quiz
from tests.outils import questions_avec_reponses

QUESTIONS = list(questions_avec_reponses().values())


def test_le_tirage_ne_contient_aucun_doublon():
    identifiants = [question["id"] for question in quiz.tirer_questions(QUESTIONS)]
    assert len(identifiants) == len(set(identifiants))


def test_le_tirage_ne_contient_que_des_questions_existantes():
    connus = {question["id"] for question in QUESTIONS}
    for question in quiz.tirer_questions(QUESTIONS):
        assert question["id"] in connus


def test_le_tirage_rend_toutes_les_questions_quand_il_y_en_a_moins_que_demande():
    docker = [question for question in QUESTIONS if question["categorie"] == "docker"]
    assert len(quiz.tirer_questions(docker)) == len(docker)
