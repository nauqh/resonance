create table if not exists playlist(
    playlist_id text primary key,           -- Playlist ID
    playlist_name text not null,            -- Playlist name
    playlist_owner text not null,           -- Playlist owner name
    playlist_description text,              -- Playlist description
    playlist_followers integer not null,    -- Playlsit no of followers
    playlist_image text not null,           -- Playlist image url
    playlist_url text not null              -- Playlsit link url
);

create table if not exists artist(
    artist_id text primary key,             -- Artist ID    
    artist_name text not null,              -- Artist name
    artist_followers integer not null,      -- Artist no of followers
    artist_genre text not null,             -- Artist genre
    artist_popularity integer not null,     -- Artist popularity (0-100)
    artist_image text not null,             -- Artist image url
    artist_url text not null                -- Artist link url
);

create table if not exists track(
    track_id text primary key,              -- Track ID
    track_name text not null,               -- Track name
    track_added_date text not null,         -- Track added date
    track_release_date text not null,       -- Track release date
    track_pop integer not null,             -- Track popularity (0 - 100)
    track_image text not null,              -- Track image url
    track_url text not null,                -- Track link url
    artist_id text not null                 -- Artist ID url (FK)
);

create table if not exists feature(
    f_track_id text primary key,            --Track ID
    f_danceability real not null,           -- Danceability (0 - 1)
    f_energy real not null,                 -- Energy (0 - 1)
    f_key integer not null,                 -- Key (-1 - 11) where -1 = not detected
    f_loudness real not null,               -- Loudness (-60 - 0)
    f_mode integer not null,                -- Mode (1 or 0)
    f_speechiness real not null,            -- Speechiness (0 - 1)
    f_acousticness real not null,           -- Acousticness (0 - 1)
    f_instrumentalness real not null,       -- Instrumentalness (0 - 1)
    f_liveness real not null,               -- Liveness (0 - 1)
    f_valence real not null,                -- Valence (0 - 1)
    f_tempo real not null,                  -- Tempo in dB
    f_duration_ms integer not null,         -- Duration in ms 
    f_time_signature integer not null       -- Time signature (3 - 7)
)

/* Note when scaling audio features
With categorical data (Mode, Key, Time signature)
    - Use one-hot encoding
    - Scaling with StandardScaler

With numerical data
    - Use StandardScaler
*/