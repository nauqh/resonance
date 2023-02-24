import base64
import pandas as pd
from stqdm import stqdm
import streamlit as st
from requests import post, get


# client_id = st.secrets["CID"]
# client_secret = st.secrets["SECRETS"]
client_id = "41ebc65d020d4aa8be24bd1f97cbd9ed"
client_secret = "62ceb3db85854f739c3fd9598504ecaf"

# TODO: Authentication


def get_token():
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


# TODO: Extract API


def get_playlist(token: str, playlist_url: str) -> dict:
    playlist_id = playlist_url.split("/")[-1].split("?")[0]
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}"
    headers = get_header(token)

    resp = get(url, headers=headers).json()
    return resp


def get_playlist_info(playlist: dict) -> dict:
    data = {}
    data['id'] = playlist['id']
    data['name'] = playlist['name']
    data['owner'] = playlist['owner']
    data['description'] = playlist['description']
    data['followers'] = playlist['followers']
    data['image'] = playlist['images'][0]['url']
    data['url'] = playlist['external_urls']['spotify']
    return data


def get_track_info(playlist: dict, index: int) -> dict:
    track = playlist['tracks']['items'][index]
    data = {}
    data['name'] = track['track']['name']
    data['added_date'] = track['added_at']
    data['release_date'] = track['track']['album']['release_date']
    data['track_id'] = track['track']['id']
    data['artist_id'] = track['track']['album']['artists'][0]['id']
    data['track_pop'] = track['track']['popularity']
    data['image'] = track['track']['album']['images'][0]['url']
    data['url'] = track['track']['external_urls']['spotify']
    return data


def get_artist_info(token: str, artist_id: str) -> dict:
    url = f"https://api.spotify.com/v1/artists/{artist_id}"
    headers = get_header(token)
    resp = get(url, headers=headers).json()

    artist = {}
    artist['artist_id'] = artist_id
    artist['name'] = resp['name']
    artist['followers'] = resp['followers']['total']
    artist['genres'] = resp['genres']
    artist['popularity'] = resp['popularity']
    if not resp['images']:
        artist['image'] = []
    else:
        artist['image'] = resp['images'][0]['url']
    artist['url'] = resp['external_urls']['spotify']
    return artist


def get_audio_features(token: str, track_id: str) -> dict:
    url = f"https://api.spotify.com/v1/audio-features/{track_id}"
    headers = get_header(token)
    resp = get(url, headers=headers).json()

    features = {}
    features['track_id'] = track_id
    features['danceability'] = resp['danceability']
    features['energy'] = resp['energy']
    features['key'] = resp['key']
    features['loudness'] = resp['loudness']
    features['mode'] = resp['mode']
    features['speechiness'] = resp['speechiness']
    features['acousticness'] = resp['acousticness']
    features['instrumentalness'] = resp['instrumentalness']
    features['liveness'] = resp['liveness']
    features['valence'] = resp['valence']
    features['tempo'] = resp['tempo']
    features['duration_ms'] = resp['duration_ms']
    features['time_signature'] = resp['time_signature']
    return features


# TODO: Utility
@st.experimental_singleton
def extract_playlist(token: str, playlist_url: str) -> tuple[dict, pd.DataFrame, pd.DataFrame]:
    playlist = get_playlist(token, playlist_url)

    # Get playlist info as dict
    playlist_info = get_playlist_info(playlist)

    # Get tracks info as dataframe
    tracks = []
    features = []

    st.write("Extracting tracks from playlist ..")
    for i in stqdm(range(len(playlist['tracks']['items']))):
        track = get_track_info(playlist, i)
        track_id = track['track_id']

        tracks.append(track)
        features.append(get_audio_features(token, track_id))
    st.success(
        f"Extracted {len(playlist['tracks']['items'])} tracks from your playlist!", icon="✅")
    track_df = pd.DataFrame(tracks)
    feature_df = pd.DataFrame(features)

    # Get artists info as dataframe
    artist_set = set(track_df['artist_id'].tolist())
    artists = []
    st.write("Extracting artists from playlist ..")
    for i in stqdm(range(len(list(artist_set)))):
        artists.append(get_artist_info(token, list(artist_set)[i]))
    artist_df = pd.DataFrame(artists)
    st.success(
        f"Extracted {len(list(artist_set))} artist from your playlist!", icon="✅")

    return playlist_info, artist_df, pd.merge(track_df, feature_df, on='track_id')


if __name__ == '__main__':
    token = get_token()
    playlist_url = 'https://open.spotify.com/playlist/4mih0AxheCVcIQaIMf1YAK?si=345baf5504f14e24'
    info, artists, features = extract_playlist(token, playlist_url)
    artists.to_csv('data/artists.csv', index=False)
    features.to_csv('data/playlist.csv', index=False)
