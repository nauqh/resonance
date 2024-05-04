from fastapi import FastAPI, status, Depends
from fastapi.middleware.cors import CORSMiddleware
import os
import json

# Database
from . import models
from .database import SessionLocal, engine
from sqlalchemy.orm import Session
from .schema import *

# Utils
from ..src.utils.utils import search_artist, search_playlist, get_recommendation
from ..src.llm import LLM
from ..src.receipt import send_email

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI(title='Resonance',
              summary="Music taste analysis and recommendation system",
              version='2.0.0')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"])


@app.get("/")
def root():
    return {"message": "Root endpoint"}


@app.post("/analysis", status_code=status.HTTP_201_CREATED)
def create_analysis(description: dict):
    return LLM(os.environ['API_KEY']).analyze(description)


@app.post("/playlist", status_code=status.HTTP_201_CREATED)
def create_playlist(playlist: Playlist):
    return search_playlist(playlist.keyword)


@app.post("/artist", status_code=status.HTTP_201_CREATED)
def create_artist(data: ArtistList):
    artists = []

    for name in data.names:
        resp = search_artist(name)
        artist = {
            "name": name,
            "img": resp['items'][0]['images'][1]['url'] or resp['items'][0]['images']['url'],
            "id": resp['items'][0]['id']}
        artists.append(artist)
    return artists


@app.post("/recommendation", status_code=status.HTTP_201_CREATED)
def create_recommendation(data: dict):
    return get_recommendation(data['ids'])


@app.post("/receipt", status_code=status.HTTP_201_CREATED)
def send_receipt(data: dict):
    send_email(data['recipients'], data['attachment'])
    return f"Sent email to {', '.join(data['recipients'])}"

# TODO: User profile


@app.post("/user", status_code=status.HTTP_201_CREATED)
def create_diagnose(data: dict, db: Session = Depends(get_db)):
    diagnose = models.Diagnose(content=json.dumps(data))
    db.add(diagnose)
    db.commit()
    return data


@app.get("/user", status_code=status.HTTP_200_OK)
def get_diagnoses(db: Session = Depends(get_db)):
    diagnoses = db.query(models.Diagnose).all()
    for diagnosis in diagnoses:
        diagnosis.content = json.loads(diagnosis.content)
    return diagnoses
