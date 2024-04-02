"""
Preprocess Spotify Million Playlist Dataset
"""
import pandas as pd
import re
import json
import os
from tqdm import tqdm
from requests import get
from pandas import DataFrame
from .utils import get_header, get_features, get_artist, get_token
from pathlib import Path


def _to_df(slide: dict) -> DataFrame:
    """
    Turn a json slide of playlists into dataframe
    """
    data = []

    for playlist in slide:
        df = pd.DataFrame(playlist)
        df_tracks = pd.DataFrame(df['tracks'].tolist())

        df_tracks["track_uri"] = df_tracks["track_uri"].apply(
            lambda x: re.findall(r'\w+$', x)[0])
        df_tracks["artist_uri"] = df_tracks["artist_uri"].apply(
            lambda x: re.findall(r'\w+$', x)[0])
        df_tracks["album_uri"] = df_tracks["album_uri"].apply(
            lambda x: re.findall(r'\w+$', x)[0])

        data.append(df_tracks)

    tracks = pd.concat(data, ignore_index=True)
    tracks.drop_duplicates(subset=['track_uri'], inplace=True)
    return tracks


def raw_to_csv(indir: str, outdir: str):
    """
    Turn slides in a directory into csv dataframe
    """
    fnames = os.listdir(indir)
    print(fnames)

    for fname in tqdm(fnames):
        with open(os.path.join(indir, fname)) as f:
            js = json.load(f)
            tracks = _to_df(js['playlists'])

            fname = fname[:-5]
            outpath = os.path.join(outdir, f'{fname}.csv')
            tracks.to_csv(outpath, index=False)


def _get_track(token: str, id: str) -> DataFrame:
    url = f"https://api.spotify.com/v1/tracks/{id}"
    headers = get_header(token)
    track = get(url, headers=headers).json()

    artist = track['artists'][0]['id']
    features = get_features(token, id)

    return pd.DataFrame([{
        'id': id,
        'name': track['name'],
        'images': track['album']['images'],
        'release_date': track['album']['release_date'],
        'url': track['external_urls']['spotify'],
        'artist': artist,
        'popularity': track['popularity'],
        **features
    }])


def csv_to_combine(path: str, token: str) -> None:
    """
    Process a slide into artists and tracks dataframe
    """
    directory = Path(path).parent.parent / 'combined'
    fnamebase = os.path.basename(path)[:-4]

    slide = pd.read_csv(path)

    # Get tracks info as dataframe
    track_ids = slide['track_uri'].tolist()
    data = [_get_track(token, id) for id in tqdm(track_ids[:10])]

    # Get artists info as dataframe
    artist_ids = slide['artist_uri'].unique()[:10]
    artists = [get_artist(token, artist_id)
               for artist_id in tqdm(artist_ids)]

    # Combine into csv
    tracks_csv_path = directory / f"tracks/{fnamebase}_tracks.csv"
    pd.concat(data, ignore_index=True).to_csv(
        tracks_csv_path, index=False)

    artists_csv_path = directory / f"artists/{fnamebase}_artists.csv"
    pd.DataFrame(artists).to_csv(artists_csv_path, index=False)


if __name__ == "__main__":
    # RAW JSON -> CSV SLIDE
    base = Path(
        'D:/Study/Monash/FIT3162/Resonance/data/Million Playlist Dataset')
    raw = base / 'raw'
    processed = base / 'processed'
    combined = base / 'combined'

    raw_to_csv(raw, processed)

    # CSV SLIDE -> ARTISTS, TRACKS
    token = get_token()
    fnames = os.listdir(processed)

    for fname in tqdm(fnames):
        print(f"\nProcess slide {fname}")
        path = os.path.join(processed, fname)
        csv_to_combine(path, token)
