"""API et interface de QuizOps."""

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from app import database, donnees, quiz

RACINE = Path(__file__).resolve().parent.parent
QUESTIONS = donnees.charger_questions()
QUESTIONS_PAR_ID = {question["id"]: question for question in QUESTIONS}

app = FastAPI(title="QuizOps")
database.initialiser()


class Reponse(BaseModel):
    question_id: int
    choix: int | None = Field(default=None, ge=0, le=3)


class Partie(BaseModel):
    pseudo: str = Field(min_length=1, max_length=30)
    reponses: list[Reponse] = Field(min_length=1)


@app.get("/api/questions")
def lister_questions(categorie: str | None = None) -> list[dict]:
    """Les questions d'une partie, sans les bonnes réponses, filtrées par catégorie si demandé."""
    questions = quiz.filtrer_par_categorie(QUESTIONS, categorie)
    if categorie is not None and not questions:
        raise HTTPException(status_code=404, detail=f"Catégorie inconnue : {categorie}")
    return [quiz.sans_reponse(question) for question in quiz.tirer_questions(questions)]


@app.get("/api/categories")
def lister_categories() -> list[str]:
    """Les catégories disponibles, triées, pour les boutons de l'interface."""
    return sorted({question["categorie"] for question in QUESTIONS})


@app.post("/api/answers")
def soumettre_reponses(partie: Partie) -> dict:
    """Reçoit les réponses d'une partie, enregistre et renvoie le score."""
    inconnus = [
        r.question_id for r in partie.reponses if r.question_id not in QUESTIONS_PAR_ID
    ]
    if inconnus:
        raise HTTPException(status_code=422, detail=f"Questions inconnues : {inconnus}")
    reponses = [reponse.model_dump() for reponse in partie.reponses]
    score = quiz.calculer_score(reponses, QUESTIONS_PAR_ID)
    database.enregistrer_score(partie.pseudo, score)
    return {"pseudo": partie.pseudo, "score": score}


@app.get("/api/scores")
def lister_scores() -> list[dict]:
    """Le classement des dix meilleurs scores."""
    return database.meilleurs_scores()


@app.get("/api/statistiques")
def afficher_statistiques() -> dict:
    """Nombre de parties jouées et score moyen."""
    return database.statistiques()


app.mount("/static", StaticFiles(directory=RACINE / "static"), name="static")


@app.get("/")
def accueil() -> FileResponse:
    return FileResponse(RACINE / "static" / "index.html")
