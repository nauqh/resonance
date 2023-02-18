from __future__ import annotations
from sqlite3 import connect
from datetime import datetime
import time
import pandas as pd


import logging
log = logging.getLogger(__name__)


class Database():
    __slots__ = ("db_path", "sql_path", "db", "cur")

    def __init__(self, db_path, build_path) -> None:
        self.db_path = db_path
        self.sql_path = build_path

    def connect(self):
        self.db = connect(self.db_path, check_same_thread=False)
        self.cur = self.db.cursor()
        self.build()
        log.info(f"📌 Connected to database at {self.db_path}")

    def build(self):
        self.scriptexec(self.sql_path)
        self.commit()

    def commit(self):
        self.db.commit()

    def close(self):
        self.db.commit()
        self.db.close()
        log.info("📌 Closed database connection")

    def record(self, command, *values):
        self.cur.execute(command, tuple(values))

        return self.cur.fetchone()

    def records(self, command, *values):
        self.cur.execute(command, tuple(values))

        return self.cur.fetchall()

    def field(self, command, *values):
        self.cur.execute(command, tuple(values))

        if (fetch := self.cur.fetchone()) is not None:
            return fetch[0]

    def execute(self, command, *values):
        self.cur.execute(command, tuple(values))

    def column(self, command, *values):
        self.cur.execute(command, tuple(values))

        return [item[0] for item in self.cur.fetchall()]

    def scriptexec(self, path):
        with open(path, 'r', encoding="utf-8") as script:
            self.cur.executescript(script.read())

    # ===================================================
    def to_date(self, text: str) -> datetime:
        """
        Convert string to datetime object

        2022-03-11T11:11:30Z
        """
        return datetime.strptime(text, '%Y-%m-%dT%H:%M:%SZ')

    def add_playlist(self, playlist: dict):
        id = playlist['id']
        name = playlist['name']
        owner = playlist['owner']['display_name']
        description = playlist['description']
        followers = playlist['followers']['total']
        image = playlist['image']
        url = playlist['url']

        querry = self.records(
            f"""SELECT * FROM playlist WHERE playlist_id = "{id}" """)
        if not querry:
            self.execute("INSERT INTO playlist VALUES (?, ?, ?, ?, ?, ?, ?)",
                         id, name, owner, description, int(followers), image, url)
            log.info(f"📌 Added {name} playlist")
        else:
            log.info(f"📌 Playlist already exists")
        self.commit()

    def add_tracks(self, df: pd.DataFrame):
        df = df.sort_values('name').reset_index(drop=True)
        count = len(df)
        for i in range(len(df)):
            id = df.loc[i, 'track_id']
            name = df.loc[i, 'name']
            added_date = df.loc[i, 'added_date']
            release_date = df.loc[i, 'release_date']
            popularity = df.loc[i, 'track_pop']
            image = df.loc[i, 'image']
            url = df.loc[i, 'url']
            artist_id = df.loc[i, 'artist_id']

            querry = self.records(
                f"""SELECT * FROM track WHERE track_id = "{id}" """)
            if not querry:
                self.execute("INSERT INTO track VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                             id, name, added_date, release_date, int(popularity), image, url, artist_id)
            else:
                count -= 1

        log.info(f"📌 Added {count} tracks")
        self.commit()

    def add_audio_features(self, df: pd.DataFrame):
        count = len(df)
        for i in range(len(df)):
            id = df.loc[i, 'track_id']
            danceability = df.loc[i, 'danceability']
            energy = df.loc[i, 'energy']
            key = df.loc[i, 'key']
            loudness = df.loc[i, 'loudness']
            mode = df.loc[i, 'mode']
            speechiness = df.loc[i, 'speechiness']
            acousticness = df.loc[i, 'acousticness']
            instrumentalness = df.loc[i, 'instrumentalness']
            liveness = df.loc[i, 'liveness']
            valence = df.loc[i, 'valence']
            tempo = df.loc[i, 'tempo']
            duration_ms = df.loc[i, 'duration_ms']
            time_signature = df.loc[i, 'time_signature']

            querry = self.records(
                f"""SELECT * FROM feature WHERE f_track_id = "{id}" """)
            if not querry:
                self.execute("INSERT INTO feature VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                             id, danceability, energy, int(key), loudness, int(mode), speechiness, acousticness, instrumentalness, liveness, valence, tempo, int(duration_ms), int(time_signature))
            else:
                count -= 1

        log.info(f"📌 Added audio features to {count} tracks")
        self.commit()

    def add_artists(self, df: pd.DataFrame):
        df = df.sort_values('name').reset_index(drop=True)
        count = len(df)
        for i in range(len(df)):
            id = df.loc[i, "artist_id"]
            name = df.loc[i, "name"]
            followers = df.loc[i, "followers"]
            genres = df.loc[i, "genres"]
            popularity = df.loc[i, "popularity"]
            image = df.loc[i, "image"]
            url = df.loc[i, "url"]

            querry = self.records(
                f"""SELECT * FROM artist WHERE artist_id = "{id}" """)
            if not querry:
                self.execute("INSERT INTO artist VALUES (?, ?, ?, ?, ?, ?, ?)",
                             id, name, int(followers), str(genres), int(popularity), image, url)
            else:
                count -= 1

        log.info(f"📌 Added {count} artists")
        self.commit()

    def artist_view(self):
        return pd.DataFrame(self.records("""select * from artist"""),
                            columns=['id', 'name', 'followers', 'genres', 'popularity', 'image', 'url'])

    def track_view(self):
        return pd.DataFrame(self.records("""select * from track"""),
                            columns=['id', 'name', 'added_date', 'release_date', 'popularity', 'image', 'url', 'artist_id'])


def insert_playlist(db, info: dict, artists: pd.DataFrame, features: pd.DataFrame):
    start = time.time()

    log.info(f"⏳ ===== {info['name']} ===== ")
    db.add_playlist(info)
    db.add_tracks(features)
    db.add_audio_features(features)
    db.add_artists(artists)

    end = time.time()
    log.info(f"⏳ Process completed in {round(end - start, 2)}s")
