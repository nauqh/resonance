import pandas as pd
import plotly.graph_objects as go


def convert_ms(ms):
    minutes = int(ms/(1000*60)) % 60
    hours = int(ms/(1000*60*60)) % 24
    return hours, minutes


def graph_features(df: pd.DataFrame) -> go.Figure:
    if (df['instrumentalness'].astype(int) == 0).all():
        df['instrumentalness'] = 0

    features = ['valence', 'energy', 'acousticness',
                'liveness', 'instrumentalness', 'danceability']
    df = df[features].mean().tolist()

    fig = go.Figure(go.Scatterpolar(
        r=df,
        theta=features,
        fill='toself',
        name='',
        hovertemplate="%{r}"
    ))
    fig.update_layout(
        template='seaborn',
        polar=dict(
            radialaxis=dict(showticklabels=False, ticks='')
        ),
        margin=dict(r=0)
    )
    return fig


def to_adj(feature):
    dictionary = {'valence': 'calming',
                  'energy': 'uplifting',
                  'danceability': 'rejuvenating',
                  'liveness': 'melodious',
                  'acousticness': 'ambient'}
    return dictionary[feature]


def analysis(df):
    """
    Find highest and lowest audio features
    """
    if (df['instrumentalness'].astype(int) == 0).all():
        df['instrumentalness'] = 0

    features = ['valence', 'energy', 'acousticness',
                'liveness', 'instrumentalness', 'danceability']
    data = df[features].mean().tolist()

    newdf = pd.DataFrame(data=data, index=features, columns=['value'])

    largest = newdf['value'].nlargest(2).index
    smallest = newdf['value'].nsmallest(2).index
    return smallest, largest


def get_top_artist(features, artists):
    top_artist_id = features['artist_id'].value_counts().index.tolist()
    names = []
    images = []
    for artist_id in top_artist_id[:4]:
        names.append(artists[artists['artist_id']
                     == artist_id]['name'].values[0])
        images.append(artists[artists['artist_id']
                      == artist_id]['image'].values[0])
    return tuple(zip(names, images))


def graph_popular_track(df: pd.DataFrame, artists: pd.DataFrame) -> go.Figure:
    """
    Visualize popular tracks 
    """
    popular = df.sort_values('track_pop', ascending=False)[
        ['name', 'artist_id', 'track_pop']][:5].reset_index(drop=True)
    popular.rename(columns={'name': 'track'}, inplace=True)
    artist_lookup = artists[['artist_id', 'name']]
    most_popular = pd.merge(popular, artist_lookup, on='artist_id', how='left')

    fig = go.Figure(go.Bar(
        x=most_popular['track_pop'],
        y=most_popular['track'],
        text=most_popular['name'],
        orientation='h',
        name='',
        marker=dict(color='#80ed99'),
        hovertemplate="%{y}<br>Popularity: %{x}"
    ))

    fig.update_layout(
        autosize=True,
        title='Most popular tracks worldwide',
        hoverlabel=dict(bgcolor='#000', font_color='#fff'),
        margin=dict(l=30, r=30, t=40),
        height=350)

    fig.update_yaxes(title=None, showticklabels=False)
    fig.update_xaxes(title=None, range=[0, 100])

    return fig


def get_obscurity(df: pd.DataFrame):
    """
    Calculate playlist obscurity 
    """
    score = df['track_pop'].mean()
    if score > 50:
        quote = "You listen to some pretty unique music! But you still enjoy top hits now and again."
    else:
        quote = "You're pretty balanced. You enjoy popular music, but also venture into the unknown."

    return df['track_pop'].mean(), quote


def get_duration(df: pd.DataFrame):
    duration = df['duration_ms'].sum()
    return round((duration/(1000*60*60)) % 24, 2)


def get_popular_artist(df: pd.DataFrame):
    res = df.loc[df['popularity'].idxmax()]
    return res['name']


def graph_timeline(df: pd.DataFrame):
    df['added_date'] = pd.to_datetime(df['added_date'])
    df['added_date'] = df['added_date'].dt.date
    data = df['added_date'].value_counts().sort_index()

    fig = go.Figure(data=go.Scatter(
        x=data.index, y=data.values, line=dict(color='#1DB954', width=3)))
    fig.update_traces(
        hoverinfo='y', hovertemplate="%{x} - %{y} tracks<extra></extra>")

    fig.update_layout(
        autosize=True,
        hoverlabel=dict(bgcolor='#000', font_color='#fff'),
        margin=dict(t=10),
        height=400)
    fig.update_yaxes(title='Number of tracks')
    fig.update_xaxes(title='Date')

    return fig
