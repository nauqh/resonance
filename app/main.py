from graph import *
from utils import *
from engine import *
import random

import streamlit as st
import streamlit.components.v1 as components


st.set_page_config(
    page_title="Resonance",
    page_icon="📡",
    layout="wide")

# TODO: Sidebar
with st.sidebar:
    st.info(
        "📌 **NOTE**: A rate limit is set to 100 requests every 2 minutes! [Details](https://github.com/nauqh/Resonance-app)")
    st.write("## About the project")
    st.markdown(
        "Resonance lets you analyze your Spotify playlists to give you a deeper understanding of your music.")
    st.markdown(
        "Resonance gathers information about your playlists using the `Spotify API` and presents the findings in a stunning way. It also lets you create new custom made playlists based on your favourite tracks.")
    st.markdown(
        "Status: `Beta`")
    st.markdown(
        "Sever shutdown on: Tue, Feb 14th, 2023 @ 1:25am (PT)")
    st.markdown("##")

# TODO: Main
st.markdown("""<h1 style='
                font-family: Recoleta-Regular; font-weight: 400;
                font-size: 3.5rem'>How Bad Is Your Spotify Playlist</h1>""",
            unsafe_allow_html=True)

st.markdown("""<h3 style='
                font-family: Recoleta-Regular; font-weight: 400;
                font-size: 1.55rem'>Our sophisticated A.I. judges your awful taste in music</h3>""",
            unsafe_allow_html=True)

"""
![Python](https://img.shields.io/badge/Made%20With-Python%203.8-blue.svg?style=for-the-badge&logo=Python)
![Plotly](https://img.shields.io/badge/plotly%20-%2300416A.svg?&style=for-the-badge&logo=plotly&logoColor=white)
"""
st.markdown("##")
st.image("img/shelf.jpeg")
url = st.text_input(
    "Please share your playlist URL (https://open.spotify.com/playlist/..)", "")
run = st.button("Find out")

if run:
    token = get_token()
    info, artists, features = extract_playlist(token, url)
    # artists.to_csv('data/artists.csv', index=False)
    # features.to_csv('data/playlist.csv', index=False)

# TODO: General info
    st.write("##")
    with st.container():
        l, r = st.columns([1, 1])
        with l:
            components.iframe(
                f"https://open.spotify.com/embed/playlist/{info['id']}?utm_source=generator", height=400)
        with r:
            st.write("##")
            st.markdown("""<span style=' 
                font-weight: 200; font-size: 1rem'>PUBLIC PLAYLIST</span>""",
                        unsafe_allow_html=True)
            st.markdown(f"""<span style='
                font-family: Recoleta-Regular; font-weight: 400;
                font-size: 3rem'>{info['name']}</span>""",
                        unsafe_allow_html=True)

            if info['description']:
                st.subheader(info['description'])
            else:
                st.subheader("Yet to have description")

            st.write(f"`Owner`: {info['owner']['display_name']}")
            st.write(f"`Content` : {len(features)} tracks")

            h, m = convert_ms(features['duration_ms'].sum())
            st.write(f"`Duration`: {h} hr {m} min")


# TODO: General mood
    with st.container():
        l, r = st.columns([1, 1])
        with l:
            adj = ['frantic', 'mellow', 'ambient', 'melodious', 'breathy', 'calming', 'monophonic',
                   'harmonious', 'dainty', 'heartfelt', 'lyrical', 'uplifting', 'synthetic', 'soulful', 'rejuvenating']
            x, y, z = random.sample(adj, 3)

            st.markdown("##")
            st.markdown("##")
            st.header(f"You have a {x}-{y}-{z} spotify")

            l, h = analysis(features)
            st.write(
                f"Based on your listening habits, I can also tell you your Spotify was.. `{to_adj(h[0])}`. It looks like the most popular songs are slightly more `{to_adj(h[1])}` and feature more `{h[1]}`.")
            st.write(
                f"They also have zero `{l[0]}` and little `{l[1]}`. I guess the important thing is that your music makes you feel good.")

        with r:
            fig = graph_features(features)
            st.plotly_chart(fig, True)

# TODO: General mood
    with st.container():
        st.header("Playlist update timeline")
        fig = graph_timeline(features)
        st.plotly_chart(fig, True)

# TODO: Top artists
    with st.container():
        st.header("You stan these artists to an uncomfortable extent")
        cols = st.columns([1, 1, 1, 1])
        top_artists = get_top_artist(features, artists)

    for i in range(len(top_artists)):
        with cols[i]:
            st.write(top_artists[i][0])
            st.image(top_artists[i][1])

# TODO: Obscurity
    fig = graph_popular_track(features, artists)
    st.markdown("##")
    st.markdown("##")
    st.header("You are too trendy for your own good")
    with st.container():
        l, r = st.columns([1, 2])
        with l:
            st.markdown("##")

            h, m = convert_ms(features['duration_ms'].sum())
            st.write(
                f"It will take `{h} hr {m} min` for someone to listen to all the songs")

            st.write(
                f"The most popular artist in your playlist is `{get_popular_artist(artists)}`")
            score, quote = get_obscurity(features)
            st.markdown(f"Your obscurity score is `{round(score, 2)}%`")
            st.markdown(quote)

        with r:
            st.plotly_chart(fig, True)


# TODO: Recommendation
    uris = recommend(features)['id']

    tracks = []
    for uri in uris:
        track = f"https://open.spotify.com/embed/track/{uri}?utm_source=generator"
        tracks.append(track)

    st.header("Here are our recommendation")
    with st.container():
        col1, col2, col3 = st.columns([1, 1, 1])
        for i in range(1, len(tracks), 3):
            with col1:
                components.iframe(tracks[i], height=352)
            with col2:
                components.iframe(tracks[i+1], height=352)
            with col3:
                components.iframe(tracks[i+2], height=352)

# NOTE: https://open.spotify.com/playlist/0UT1JN2PGg2Uitze6ujdl4?si=6ec3fc6868c044ab
