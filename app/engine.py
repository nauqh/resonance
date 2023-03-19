import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity


class Pipeline():
    def __init__(self):
        pass

    def select_cols(self, df):
        return df[['track_id', 'danceability', 'energy', 'key', 'loudness', 'mode',
                   'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'track_pop']]

    def ohe(self, df: pd.DataFrame, column: str, new_name: str):
        tf_df = pd.get_dummies(df[column])
        tf_df.columns = [new_name + "|" + str(i) for i in tf_df.columns]
        tf_df.reset_index(drop=True, inplace=True)
        return tf_df

    def create_feature_set(self, df, float_cols) -> pd.DataFrame:
        scaler = StandardScaler()

        # One-hot Encoding
        key_ohe = self.ohe(df, 'key', 'key')
        key_ohe = pd.DataFrame(scaler.fit_transform(
            key_ohe), columns=key_ohe.columns)
        mode_ohe = self.ohe(df, 'mode', 'mode')
        mode_ohe = pd.DataFrame(scaler.fit_transform(
            mode_ohe), columns=mode_ohe.columns)

        # Scale popularity columns
        pop = df[["track_pop"]].reset_index(drop=True)
        pop_scaled = pd.DataFrame(
            scaler.fit_transform(pop), columns=pop.columns)

        # Scale audio columns
        floats = df[float_cols].reset_index(drop=True)
        floats_scaled = pd.DataFrame(
            scaler.fit_transform(floats), columns=floats.columns)

        # Concanenate all features
        final = pd.concat([floats_scaled, pop_scaled,
                          key_ohe, mode_ohe], axis=1)

        # Add song id
        final['id'] = df['track_id'].values

        return final

    def create_playlist_vector(self, playlist: pd.DataFrame) -> list:
        """
        Summarize user's playlist into a single vector
        """
        playlist = playlist.drop(columns="id")

        return playlist.sum(axis=0)

    def create_repository(self, features: pd.DataFrame, playlist: pd.DataFrame) -> pd.DataFrame:
        """
        Generate features repository of songs not in playlist

        Args:
            features: song features dataframe
            playlist: playlist song features dataframe
        """

        cols = list(playlist.columns)

        # Select features of songs which are not in playlist
        repository = features[~features['id'].isin(playlist['id'].values)]

        for col in cols:
            if col not in repository.columns:
                repository[col] = 0

        return repository[cols]

    def recommendation(self, playlist_vector: list, feature_repo: pd.DataFrame) -> pd.DataFrame:
        '''
        Generated recommendation based on songs in a specific playlist.

        Args: 
            df (dataframe): spotify dataframe
            playlist_vector (series): summarized playlist feature (single vector)
            repository (dataframe): feature set of songs that are not in the selected playlist

        Returns: 
            Top 10 recommendations for the playlist
        '''
        suggest = pd.DataFrame(feature_repo['id'])
        suggest['sim'] = cosine_similarity(feature_repo.drop('id', axis=1).values,
                                           playlist_vector.values.reshape(1, -1))[:, 0]

        result = suggest.sort_values('sim', ascending=False).head(10)
        result = result.reset_index(drop=True)
        return result


def recommend(playlist: pd.DataFrame):
    features = pd.read_csv("data/features.csv")
    float_cols = playlist.dtypes[playlist.dtypes == 'float64'].index.values

    pl = Pipeline()
    playlist = pl.select_cols(playlist)
    playlist = pl.create_feature_set(
        playlist, float_cols=float_cols)
    playlist_vector = pl.create_playlist_vector(playlist)
    repository = pl.create_repository(features, playlist)
    return pl.recommendation(playlist_vector, repository)


if __name__ == '__main__':
    pass
    # playlist = pd.read_csv("data/playlist.csv")
    # print(recommend(playlist)['id'].tolist())
