# 🎧Resonance - A music recommendation system

![Python](https://img.shields.io/badge/Made%20With-Python%203.10-blue.svg?&style=for-the-badge&logo=python&logoColor=white&colorB=00b4d8)
![React](https://img.shields.io/badge/react-%2320232a.svg?style=for-the-badge&logo=react&logoColor=white&&colorB=00b4d8)
![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white&colorB=0096c7)

![ChatGPT](https://img.shields.io/badge/chatGPT-74aa9c?style=for-the-badge&logo=openai&logoColor=white)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white&colorB=52b788)
![Spotify](https://img.shields.io/badge/Spotify-1ED760?style=for-the-badge&logo=spotify&logoColor=white)

**Update** (9 November 2023): View the web application here at [Resonance](https://resonance.streamlit.app/)

## About the project

In the contemporary era of digital music consumption, music enthusiasts have unparalleled access to a vast ocean of musical content. However, within these expansive collections, the need to discover the ideal tunes can be simultaneously delightful and difficult. 

Our project since then was initiated from a keen aspiration to directly address this challenge by contructing an innovative and efficient Music Recommendation System which leverages both existing data provided by music streaming platform and contemporary technology of recommender engine and large language models.

<img  width="500" src="./img/shelf.jpeg">

## Spotify Million Playlist Dataset
The foundation of the recommendation engine will hinge upon the [Spotify Million Playlist](https://www.aicrowd.com/challenges/spotify-million-playlist-dataset-challenge) dataset, a substantial corpus curated for the purpose of advancing research in music recommendations. Sampled from the over 4 billion public playlists on Spotify, this dataset of 1 million playlists consist of over 2 million unique tracks by nearly 300,000 artists, and represents the largest public dataset of music playlists in the world. The dataset includes public playlists created by US Spotify users between January 2010 and November 2017. 

The challenge ran from January to July 2018, and received 1,467 submissions from 410 teams. A summary of the challenge and the top scoring submissions was published in the [ACM Transactions on Intelligent Systems and Technology](https://dl.acm.org/doi/abs/10.1145/3344257).

## Data Management

<img  width="1000" src="./img/Components.png">

### 1. Extraction

Our project revolves around refining the Spotify Million Playlist Dataset. We achieve this by meticulously cleaning the data, resulting in approximately 600,000 unique track identifiers (URIs). These URIs form the bedrock for interfacing with the Spotify API, allowing us to retrieve both audio characteristics and associated metadata for each track. This, in turn, enables us to develop a recommendation system finely tuned to individual user preferences.

Rather than utilizing the complete original dataset for training our recommendation engine, we've chosen a different approach due to limitations and inconsistencies in the JSON format. Instead, we've crafted a comprehensive solution that revolves around creating a customized dataset, with the Million Playlist Dataset at its core. This process involves the initial extraction of all song URLs, followed by a meticulous data aggregation and cleaning process. The goal here is to isolate unique URIs while eliminating any duplications.

Through this meticulous approach, we gather essential audio features and pertinent song metadata, which includes artist and album details. This carefully curated dataset will serve as the cornerstone of our recommendation engine, ensuring that users receive highly relevant results through our interface. 

Additional details about the data can be accessed via the [Spotify Developer](https://developer.spotify.com/documentation/web-api) platform. The code for the extraction process can be found in the associated [repository](https://github.com/nauqh/Resonance).

### 2. Storage 

<img  width="800" src="./img/storage.png">

Following the extraction process, the acquired data will be subsequently loaded into a centralized database for further processing, which includes transformation into a machine-readable format. As outlined in the preceding section, the data obtained from the Spotify API comprises three primary categories:
- **Artist data** encompasses comprehensive information pertaining to the performing artist, including but not limited to genres, popularity, images, and external urls.
- **Song metadata** contains a diverse set of attributes related to the song, encompassing details such as genres, album information, release date, and popularity.
- **Audio features** encapsulates audio-related metrics for a given song, encompassing factors such as valence, danceability, mode, loudness, and instrumentalness.

### 3. Transformation

A critical aspect of preprocessing techniques employed in this procedure centers on two fundamental tasks: the normalization of numeric data and the computation of term frequencies for categorical data.

#### Data normalization

In the context of recommendation systems, data normalization plays a crucial role in ensuring that relevant variables are consistently scaled, thereby facilitating precise computations. Specifically, in the case of numeric audio features data, normalization is imperative to establish a uniform basis for comparisons and to prevent potential distortions in recommendation outcomes. To this end, we have harnessed the capabilities of the **MinMaxScaler()** function from the scikit-learn library, a highly potent tool adept at automatically standardizing values within a defined range of 0 to 1. 

#### Categorical data encoding

TF-IDF, also known as [Term Frequency-Inverse Document Frequency](https://en.wikipedia.org/wiki/Tf%E2%80%93idf), is a tool to quantify words in a set of documents. The goal of TF-IDF is to show the importance of a word in the documents and the corpus. The general formula for calculating TF-IDF score is:

<img  width="800" src="./img/tfidf.webp">

The motivation is to find words that are not only important in each document but also accounting for the entire corpus. The log value was taken to decrease the impact of a large N, which would lead to a very large IDF compared to TF. Term Frequency (TF) focuses on how crucial a word is within one document, while Inverse Document Frequency (IDF) looks at how important a word is across all the documents.

## Recommendation Engine

### 1. Content-based Filtering

Content-based Filtering is a recommender technique that uses unique features of items to find similar ones. It assigns a similarity score based on these features to generate recommendations. In the case of Spotify playlists, this involves analyzing song characteristics to compute an aggregate score for a playlist. Then, it recommends top similar songs that closely align with this score but are not already in the playlist.

The [K-Nearest Neighbor (KNN)](https://en.wikipedia.org/wiki/K-nearest_neighbors_algorithm) algorithm is commonly used in Content-based Filtering for music recommendation systems. It works by finding a specified number (K) of music tracks that closely match a user's current preferences. This is done by comparing features like genre, tempo, instrumentation, and user behavior patterns. By utilizing this similarity metric, KNN can make accurate predictions about which songs a user is likely to enjoy based on their past interactions with the platform.

<img  width="800" src="./img/knn.webp">

### 2. Data Pipeline

A specialized data pipeline has been crafted to serve this objective, structured around two distinct use cases. In the scenario where users opt to furnish their own Spotify playlists as input, the pipeline initiates with the retrieval of diverse Spotify URIs within the user playlist, accompanied by their corresponding audio features and metadata. 

<img  width="500" src="./img/input.png">

Following this, the system engages in a filtering process to remove URIs that are already present within the database. Subsequently, user playlist undergoes transformation into a unified vector of quantitative values, achieved through the application of mean summarization.

The resultant vector obtained here acts as a test point for the **K-Nearest Neighbors** algorithm. This allows us to calculate distances between the playlist vector and other songs in the dataset. The top neighbors are then chosen and ranked in ascending order. It's important to highlight that the data point closest to the input features receives the highest rank. If users provide specific audio features, the system will exclusively use these attributes for generating recommendations using the KNN algorithm.

```python
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
```

### 3. Music Taste Analysis

In addition to providing song recommendations tailored to the user preferences, we have implemented a text-based system that offers a comprehensive analysis of individualized music characteristics, drawing insights from the user's specific music taste. 

The primary objective of the **Music Taste Analysis** engine is to evaluate user musical preferences based on their specified criteria. This assessment yields a comprehensive explanation of the user’s music tastes, accompanied by a thoughtfully curated selection of musical artists that align with these preferences. 

<img  width="500" src="./img/musictaste.png">
