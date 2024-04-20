from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from ..src.utils.utils import search_artist, search_playlist, get_recommendation
from ..src.llm import LLM
import os


app = FastAPI(title='Resonance', version='2.0.0')

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
def create_playlist(data: dict):
    return search_playlist(data['keyword'])


@app.post("/artist", status_code=status.HTTP_201_CREATED)
def create_artist(data: dict):
    artists = []

    for name in data['names']:
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
    ...
