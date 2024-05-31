from fastapi import FastAPI, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Database
from . import models
from .database import engine
from .schemas import Playlist, ArtistList

# Utils
from ..src.utils.utils import search_artist, search_playlist, get_recommendation
from ..src.llm import LLM
from ..src.receipt import send_email

# Routers
from .routers import user

models.Base.metadata.create_all(bind=engine)


app = FastAPI(title='Resonance',
              summary="Music taste analysis and recommendation system",
              version='2.0.0')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"])

app.include_router(user.router)


@app.get("/")
def root():
    return {"message": "Root endpoint"}


@app.post("/analysis", status_code=status.HTTP_201_CREATED)
def create_analysis(data: dict):
    try:
        response = LLM(data['key']).analyze(data['description'])
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid API key")
    return response


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
