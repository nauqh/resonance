import pandas as pd
# from ast import literal_eval

from wordcloud import WordCloud
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# =======================================
# TODO: Utils


def convert_ms(ms):
    minutes = int(ms/(1000*60)) % 60
    hours = int(ms/(1000*60*60)) % 24
    return hours, minutes


def to_adj(feature):
    dictionary = {'valence': 'calming',
                  'energy': 'uplifting',
                  'danceability': 'rejuvenating',
                  'liveness': 'melodious',
                  'acousticness': 'ambient'}
    return dictionary[feature]


def analysis(df):
    if (df['instrumentalness'].astype(int) == 0).all():
        df['instrumentalness'] = 0

    features = ['valence', 'energy', 'acousticness',
                'liveness', 'instrumentalness', 'danceability']
    data = df[features].mean().tolist()

    newdf = pd.DataFrame(data=data, index=features, columns=['value'])

    largest = newdf['value'].nlargest(2).index
    smallest = newdf['value'].nsmallest(2).index
    return smallest, largest


def get_obscurity(df: pd.DataFrame):
    """
    Calculate playlist obscurity 
    """
    score = df['track_pop'].mean()
    if score > 50:
        quote = "You listen to some pretty unique music! But you still enjoy top hits now and again."
    else:
        quote = "You're pretty balanced (or low-key tbh). You enjoy popular music, but also venture into the unknown."

    return df['track_pop'].mean(), quote


def get_duration(df: pd.DataFrame):
    duration = df['duration_ms'].sum()
    return round((duration/(1000*60*60)) % 24, 2)


def get_popular_artist(df: pd.DataFrame):
    res = df.loc[df['popularity'].idxmax()]
    return res['name']


def get_top_artist(features, artists):
    top_artist_id = features['artist_id'].value_counts().index.tolist()
    names = []
    images = []
    for artist_id in top_artist_id[:6]:
        artist_name = artists[artists['artist_id']
                              == artist_id]['name'].values[0]
        if artist_name != "Various Artists":
            names.append(artist_name)
            images.append(artists[artists['artist_id'] ==
                          artist_id]['image'].values[0])
    return tuple(zip(names, images))[:5]

# =============================================
# TODO: Utils


def graph_features(df: pd.DataFrame) -> go.Figure:
    # Normalize loudness to 0-1 scale
    df['loudness'] = (df['loudness']-min(df['loudness'])) / \
        (max(df['loudness'])-min(df['loudness']))
    if (df['instrumentalness'].astype(int) == 0).all():
        df['instrumentalness'] = 0

    features = ['valence', 'energy', 'acousticness', 'instrumentalness',
                'liveness', 'loudness', 'danceability']
    features = [*features, features[0]]
    df = df[features].mean().tolist()

    fig = go.Figure(go.Scatterpolar(
        r=df,
        theta=features,
        fill='toself',
        name='',
        hovertemplate="%{r:,.2f}",
        fillcolor='#1db954',
        line_color='#1ed760',
        opacity=0.5,
    ))
    fig.update_layout(
        template='seaborn',
        polar=dict(
            radialaxis=dict(showticklabels=True, ticks='',
                            color='#000', tickfont_size=10),
            angularaxis=dict(direction="clockwise", color='#000'),
            bgcolor='#adf7b6'
        ),
        margin=dict(t=20, b=20, l=0, r=0),
        hoverlabel=dict(bgcolor='#000', font_color='#fff'),
        height=350
    )
    return fig


def graph_audio_proportion(names, dances, energies, lives):
    # Calculate the sum of danceability, energy, and liveness for each genre
    sums = [d + e + l for d, e, l in zip(dances, energies, lives)]

    # Sort names based on the sum of danceability, energy, and liveness
    sorted_data = sorted(
        zip(names, dances, energies, lives, sums), key=lambda x: x[4])
    names, dances, energies, lives, _ = zip(*sorted_data)

    fig = go.Figure()

    types = ['Danceability', 'Energy', 'Liveness']
    colors = ['#8eecf5', '#98f5e1',  '#b9fbc0']

    for type, color in zip(types, colors):
        fig.add_trace(go.Bar(
            y=names,
            x=dances if type == 'Danceability' else (
                energies if type == 'Energy' else lives),
            name=type,
            orientation='h',
            marker=dict(color=color, line=dict(color='#000', width=1)),
            hovertemplate='%{x:,.2f}'
        ))

    fig.update_layout(title='Dancing Elements Proportion', barmode='stack', title_font_size=18,
                      height=400,
                      hoverlabel=dict(bgcolor='#161513', font_color='#fff'),
                      legend=dict(orientation="h", yanchor="top",
                                  xanchor="center", x=0.5, y=1.1),
                      margin=dict(t=30, b=10, l=0, r=0),
                      xaxis=dict(tickfont=dict(color='#000')),
                      yaxis=dict(tickfont=dict(color='#000')))

    return fig


def graph_popular_track(df: pd.DataFrame) -> go.Figure:
    popular = df.sort_values('track_pop', ascending=False)[
        ['name', 'artist_id', 'track_pop']][:6].reset_index(drop=True)
    fig = go.Figure(go.Bar(
        y=popular['name'],
        x=popular['track_pop'],
        orientation='h',
        marker=dict(
            color=['#98f5e1' if i == popular['track_pop'].idxmax(
            ) else '#b9fbc0' for i in range(len(popular))],
            line=dict(color='#000', width=1)
        ),
        hovertemplate="Popularity: %{x} <extra></extra>"
    ))

    fig.update_layout(
        autosize=True,
        title='Popular Tracks Worldwide', title_font_size=20,
        hoverlabel=dict(bgcolor='#000', font_color='#fff'),
        margin=dict(l=0, r=0, t=30),
        height=350,
        xaxis=dict(tickfont=dict(color='#000')),
        yaxis=dict(tickfont=dict(color='#000')))

    fig.update_yaxes(showgrid=False, title=None)
    fig.update_xaxes(title="Popularity (%)", range=[
                     0, 100], title_font_color="#000")

    return fig


def graph_decades(df):
    years_series = pd.to_datetime(df['release_date'], format='mixed')
    decades = (years_series.dt.year // 10 * 10).astype(str)
    decade_counts = decades.value_counts().sort_index()

    colors = ['#b9fbc0', '#98f5e1', '#8eecf5',
              '#90dbf4', '#a3c4f3', '#cfbaf0', 'f1c0e8']

    labels = decade_counts.sort_index().index.astype(str) + 's'
    fig = go.Figure(data=[go.Pie(labels=labels, values=decade_counts.values, hole=0.4, sort=False,
                                 direction='clockwise', pull=[0.1]*len(decade_counts.index))])

    fig.update_traces(name='', textinfo='none',
                      hovertemplate='Decade: %{label}<br>Tracks: %{value}',
                      marker=dict(colors=colors, line=dict(color='#000', width=1)))

    fig.update_layout(
        title="Track by decades", title_font_size=18,
        margin=dict(t=30, l=0, r=0),
        legend=dict(
            x=0,
            y=1,
            font=dict(size=15)
        ),
        height=400
    )

    return fig


def graph_decade_percent(df):
    years_series = pd.to_datetime(df['release_date'], format='mixed')
    decade_counts = (years_series.dt.year // 10 *
                     10).astype(str).value_counts(normalize=True) * 100

    # Data
    categories = ['Others', decade_counts.idxmax() + 's']
    values = [100 - decade_counts.max(), decade_counts.max()]

    # Create figure
    fig = go.Figure()

    # Add horizontal bar trace
    fig.add_trace(go.Bar(
        y=categories,
        x=values,
        orientation='h',
        hovertemplate="%{x}% <extra></extra>",
        marker=dict(
            color=['#a3c4f3' if category ==
                   "Others" else '#cfbaf0' for category in categories],
            line=dict(color='#000', width=1)
        ),
    ))

    # Update layout
    fig.update_layout(
        template='seaborn',
        title='Most listened decade',
        title_font_size=18,
        height=200,
        margin=dict(t=40, b=0, l=0, r=0),
        xaxis=dict(title=None),
        yaxis=dict(title=None, showgrid=False),
    )

    return fig, decade_counts.idxmax() + 's', len(decade_counts.index)


def graph_timeline(df: pd.DataFrame):
    df['added_date'] = pd.to_datetime(df['added_date']).dt.date

    # Now you can perform your groupby operation
    data = df.groupby('added_date').agg(
        {'track_id': 'nunique', 'track_pop': 'mean'})

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(go.Scatter(x=data.index, y=data['track_id'], name="No of Tracks",
                             line_width=3, hovertemplate='Tracks: %{y} <extra></extra>'), secondary_y=False)

    fig.add_trace(go.Scatter(x=data.index, y=data['track_pop'], name="Track Pop",
                             line_width=3, hovertemplate='Popularity: %{y:.1f} <extra></extra>'), secondary_y=True)

    fig.update_layout(title="Popularity by Number of Track added", title_font_size=18,
                      height=400,
                      autosize=True,
                      legend=dict(orientation="h", yanchor="top",
                                  xanchor="center", x=0.5, y=1.1),
                      margin=dict(t=30, b=10, l=0, r=0),
                      hovermode='x unified')

    fig.update_yaxes(title="No of Tracks", secondary_y=False,
                     showgrid=False, zeroline=False)
    fig.update_yaxes(title="Popularity", secondary_y=True,
                     range=[0, 100], showgrid=False)
    fig.update_xaxes(title=None, showgrid=False)

    return fig


def graph_genres(df):
    # df['genres'] = df['genres'].apply(literal_eval)
    genres_count = pd.Series([x for _list in df['genres']
                             for x in _list]).value_counts().to_dict()
    if "alt z" in genres_count:
        genres_count['hip hop'] = genres_count.pop('alt z')

    # Generate wordcloud
    wordcloud = WordCloud(width=1600, height=800,
                          background_color='#fafafa').generate_from_frequencies(genres_count)

    # Plot the wordcloud
    plt.figure(figsize=(20, 10), frameon=False)
    plt.imshow(wordcloud)
    plt.axis('off')
    plt.tight_layout(pad=0)

    return plt
