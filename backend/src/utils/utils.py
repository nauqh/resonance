import base64
from tqdm import tqdm
import pandas as pd
from pandas import DataFrame
from requests import post, get
from dotenv import load_dotenv
import os

load_dotenv()


client_id = os.environ['ID']
client_secret = os.environ['SECRET']


def get_token() -> str:
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}

    resp = post(url, headers=headers, data=data).json()
    token = resp["access_token"]

    return token


def get_header(token: str):
    return {"Authorization": "Bearer " + token}


# TODO: EXTRACT
def search_artist(name: str) -> dict:
    token = get_token()
    url = f"https://api.spotify.com/v1/search?q={name.replace(' ', '%20')}&type=artist&limit=1"
    headers = get_header(token)
    return get(url, headers=headers).json()['artists']


def get_playlist(playlist_url: str) -> dict:
    token = get_token()
    playlist_id = playlist_url.split("/")[-1].split("?")[0]
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}"
    headers = get_header(token)

    resp = get(url, headers=headers).json()
    return resp


def get_artist(artist_id: str) -> dict:
    token = get_token()
    url = f"https://api.spotify.com/v1/artists/{artist_id}"
    headers = get_header(token)
    return get(url, headers=headers).json()


def get_features(track_id: str) -> dict:
    token = get_token()
    url = f"https://api.spotify.com/v1/audio-features/{track_id}"
    headers = get_header(token)
    return get(url, headers=headers).json()


def extract_tracks(playlist) -> DataFrame:
    tracks = []
    for track in tqdm(playlist['tracks']['items']):
        id, name, images, added_date, release_date, url, popularity = (
            track['track']['id'],
            track['track']['name'],
            track['track']['album']['images'],
            track['added_at'],
            track['track']['album']['release_date'],
            track['track']['external_urls']['spotify'],
            track['track']['popularity']
        )
        artist = track['track']['artists'][0]['id']
        features = get_features(id)

        tracks.append({
            'id': id,
            'name': name,
            'images': images,
            'added_date': added_date,
            'release_date': release_date,
            'url': url,
            'artist': artist,
            'popularity': popularity,
            **features
        })
    return pd.DataFrame(tracks)


def search_playlist(keyword: str) -> dict:
    token = get_token()
    url = f"https://api.spotify.com/v1/search?q={keyword.replace(' ', '%20')}&type=playlist&limit=1"
    headers = get_header(token)
    return get(url, headers=headers).json()['playlists']['items'][0]


def get_recommendation(artist_ids: list):
    token = get_token()
    url = f"https://api.spotify.com/v1/recommendations?seed_artists={','.join(artist_ids)}&limit=9"
    headers = get_header(token)
    tracks = get(url, headers=headers).json()['tracks']

    return [{'id': track['id'],
             'name': track['name'],
             'artist': track['artists'][0]['name'],
             'duration': f"{track['duration_ms'] // 60000}:{(track['duration_ms'] % 60000) / 1000:02.0f}"
             } for track in tracks]


def extract_artists(df) -> DataFrame:
    token = get_token()
    ids = {row['artist'] for _, row in df.iterrows()}
    artists = [get_artist(token, id) for id in tqdm(ids)]
    return pd.DataFrame(artists)


if __name__ == "__main__":
    artist = search_artist("Justin Bieber")
    print(artist)

    artist_ids = ['1uNFoZAHBGtllmzznpCI3s', '5IH6FPUwQTxPSXurCrcIov']
    get_recommendation(artist_ids)
