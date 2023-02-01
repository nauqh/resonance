import re
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity
from utils import extract_playlist


class Pipeline():
    def __init__(self) -> None:
        pass

    def select_cols(self, df):
        return df[['track_id', 'danceability', 'energy', 'key', 'loudness', 'mode',
                   'speechiness', 'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'track_pop', 'time_signature']]

    def ohe(self, df: pd.DataFrame, column: str, new_name: str):
        """
        Create One Hot Encoded features of a specific column

        Args: 
            df: Spotify Dataframe
            column: Column to be processed
            new_name: new column name to be used

        Return: 
            tf_df: One-hot encoded features 
        """

        tf_df = pd.get_dummies(df[column])
        tf_df.columns = [new_name + "|" + str(i) for i in tf_df.columns]
        tf_df.reset_index(drop=True, inplace=True)
        return tf_df

    def create_feature_set(self, df, float_cols) -> pd.DataFrame:
        """
        Process spotify df to create a final set of features that will be used to generate recommendations

        Args: 
            df: Spotify Dataframe
            float_cols: List of float columns that will be scaled

        Returns: 
            Final set of features 
        """

        # One-hot Encoding
        key_ohe = self.ohe(df, 'key', 'key') * 0.5
        mode_ohe = self.ohe(df, 'mode', 'mode') * 0.5
        time_ohe = self.ohe(df, 'time_signature', 'time_signature') * 0.5

        # Normalization
        # Scale popularity columns
        pop = df[["track_pop"]].reset_index(drop=True)
        scaler = MinMaxScaler()
        pop_scaled = pd.DataFrame(
            scaler.fit_transform(pop), columns=pop.columns) * 0.2

        # Scale audio columns
        floats = df[float_cols].reset_index(drop=True)
        scaler = MinMaxScaler()
        floats_scaled = pd.DataFrame(scaler.fit_transform(
            floats), columns=floats.columns) * 0.2

        # Concanenate all features
        final = pd.concat([floats_scaled, pop_scaled,
                          key_ohe, mode_ohe, time_ohe], axis=1)

        # Add song id
        final['id'] = df['track_id'].values

        return final

    def create_playlist_vector(self, playlist: pd.DataFrame) -> list:
        """
        Summarize user's playlist into a single vector

        Args:
            playlist: dataset of song playlist

        Returns:
            Dataframe of playlist audio features
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
    playlist = pl.create_feature_set(
        playlist, float_cols=float_cols)
    playlist_vector = pl.create_playlist_vector(playlist)
    repository = pl.create_repository(features, playlist)
    return pl.recommendation(playlist_vector, repository)


if __name__ == '__main__':
    playlist = pd.read_csv("data/playlist.csv")
    print(recommend(playlist)['id'].tolist())
