from engine import *
from graph import *
from utils import *
import random

import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="Resonance",
    page_icon="img/favicon.png",
    layout="wide")

_, m, _ = st.columns([0.1, 1, 0.1])
with m:
    st.markdown("""<h3 style='
                font-family: "Inconsolata"; font-weight: 400;
                font-size: 3rem'>How Sick Is Your Spotify Playlist?</h3>""",
                unsafe_allow_html=True)

    st.markdown("""<h3 style='
                font-family: "Inconsolata"; font-weight: 400;
                font-size: 1.4rem'>Our overtime service refines your awful taste in music</h3>""",
                unsafe_allow_html=True)
    """
    ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=fafafa)
    ![Plotly](https://img.shields.io/badge/plotly%20-%2300416A.svg?&style=for-the-badge&logo=pandas&logoColor=white)
    ![ChatGPT](https://img.shields.io/badge/chatGPT-74aa9c?style=for-the-badge&logo=openai&logoColor=white)
    ![Spotify](https://img.shields.io/badge/Spotify-1ED760?style=for-the-badge&logo=spotify&logoColor=white)
    """
    st.image("img/shelf.jpeg")
    url = st.text_input("Input your Spotify playlist")

    run = st.button("Find out")
    if st.button("Try sample playlist"):
        url = "https://open.spotify.com/playlist/2xukpbxolEK8C9HdpANzZu?si=b6f9f35f63f24089"
        run = True

if run:
    token = get_token()
    info, artists, features = extract_playlist(token, url)

    # artists.to_csv('data/artists.csv', index=False)
    # features.to_csv('data/playlist.csv', index=False)


# TODO: General info
    st.markdown("##")
    st.markdown("##")
    _, m, _ = st.columns([0.1, 1, 0.1])
    with m:
        l, r = st.columns([1, 1])
        with l:
            components.iframe(
                f"https://open.spotify.com/embed/playlist/{info['id']}?utm_source=generator", height=500)
        with r:
            st.write("##")
            st.markdown("PUBLIC PLAYLIST")
            st.markdown(f"""<span style='
                font-family: Recoleta-Regular; font-weight: 400;
                font-size: 2rem'>{info['name']}</span>""",
                        unsafe_allow_html=True)

            if info['description']:
                st.write(info['description'])
            else:
                st.subheader("Yet to have description")

            st.write(f"`Owner`: {info['owner']['display_name']}")
            st.write(f"`Content` : {len(features)} tracks")

            h, m = convert_ms(features['duration_ms'].sum())
            st.write(f"`Duration`: {h} hr {m} min")


# TODO: General mood
        l, r = st.columns([1, 1])
        with l:
            adj = ['frantic', 'mellow', 'ambient', 'melodious', 'breathy', 'calming', 'monophonic',
                   'harmonious', 'dainty', 'heartfelt', 'lyrical', 'uplifting', 'synthetic', 'soulful', 'rejuvenating']
            x, y, z = random.sample(adj, 3)

            st.markdown("##")
            st.subheader("Playlist mood")
            st.write(f"You have a `{x}-{y}-{z}` spotify")

            l, h = analysis(features)
            st.write(
                f"Based on your listening habits, I can also tell you your Spotify was.. `{to_adj(h[0])}`. It looks like the most popular songs are slightly more `{to_adj(h[1])}` and feature more `{h[1]}`.")
            st.write(
                f"They also have zero `{l[0]}` and little `{l[1]}`. I guess the important thing is that your music makes you feel good.")

        with r:
            fig = graph_features(features)
            st.plotly_chart(fig, True)

# TODO: Audio features proportion
        df = pd.merge(
            features, artists[['artist_id', 'genres']], on='artist_id')
        df['genres'] = df['genres'].apply(lambda x: x[0] if x else None)

        dance = df.groupby('genres')['danceability'].mean().to_dict()
        energy = df.groupby('genres')['energy'].mean().to_dict()
        live = df.groupby('genres')['liveness'].mean().to_dict()

        names = list(dance.keys())
        dances = list(dance.values())
        energies = list(energy.values())
        lives = list(live.values())

        fig = graph_audio_proportion(names, dances, energies, lives)
        st.plotly_chart(fig, True)

# TODO: Obscurity
        fig = graph_popular_track(features)
        st.markdown("##")

        l, r = st.columns([1, 3])
        with l:
            st.markdown("##")
            st.markdown("##")
            h, m = convert_ms(features['duration_ms'].sum())
            st.write(
                f"""It will take `{h} hr {m} min` for someone to listen to all the songs.
                The most popular artist in your playlist is `{get_popular_artist(artists)}`""")

            score, quote = get_obscurity(features)
            st.markdown(
                f"Your obscurity score is `{round(score, 2)}%`. {quote}")

        with r:
            st.markdown("##")
            st.plotly_chart(fig, True)

# TODO: PLaylist update time
        tabl, tabr = st.tabs(["By decade", "By date"])
        with tabl:
            l, r = st.columns([1.2, 1])
            with l:
                fig = graph_decades(features)
                st.plotly_chart(fig, True)
            with r:
                fig, decade, decade_count = graph_decade_percent(features)
                st.write(f"""
                You're a musical time traveler! You've been listening to music made from a whopping `{decade_count} decades`. Your favorite decade of music is the `{decade}`.
                Check out songs you’ve been listening to in each decade.
                """)
                st.plotly_chart(fig, True)

        with tabr:
            fig = graph_timeline(features)
            st.plotly_chart(fig, True)

# TODO: Top artists
        st.subheader("You stan these artists to an uncomfortable extent")
        cols = st.columns([1, 1, 1, 1, 1])
        top_artists = get_top_artist(features, artists)

        for i in range(len(top_artists)):
            with cols[i]:
                st.write(top_artists[i][0])
                st.image(top_artists[i][1])

# TODO: Genres
        st.markdown("##")
        st.subheader("Your beloved genres")
        fig = graph_genres(artists)
        st.pyplot(fig, use_container_width=True)

# TODO: Recommendation
        uris = recommend(features)['id']

        tracks = []
        for uri in uris:
            track = f"https://open.spotify.com/embed/track/{uri}?utm_source=generator"
            tracks.append(track)

        st.markdown("##")
        st.subheader("Your music resonates with these tastes")
        col1, col2, col3 = st.columns([1, 1, 1])
        for i in range(1, len(tracks), 3):
            with col1:
                components.iframe(tracks[i], height=352)
            with col2:
                components.iframe(tracks[i+1], height=352)
            with col3:
                components.iframe(tracks[i+2], height=352)

        # TODO: Footer
        st.markdown("##")
        st.markdown(
            "This is a satirical project that leverages large language model for music taste analysis and recommendation. The system engine incorporates a custom blend of insights generated by OpenAI's [GPT-4](https://platform.openai.com/docs/models/gpt-4-and-gpt-4-turbo) model paired with recommendation derived from comprehensive data obtained through [Spotify API](https://developer.spotify.com/documentation/web-api).")
        st.markdown(
            "Further explore your music taste with our main clinice, [Musicotherapy](https://musicotherapy.vercel.app).")
        st.markdown("""Follow our latest updates on Github. <iframe src="https://ghbtns.com/github-btn.html?user=nauqh&repo=resonance-app&type=star&count=true" width="150" height="20" title="GitHub"></iframe>
                    """, unsafe_allow_html=True)
        st.markdown("""A project by <a href="https://nauqh.github.io/" style='
                font-family: "Inconsolata"; font-weight: 500; color: #000;
                font-size: 2rem'>nauqh</a>""",
                    unsafe_allow_html=True)
