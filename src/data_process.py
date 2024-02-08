import pandas as pd 
from typing import List

def preprocess_data(
        data: pd.DataFrame,
        ) -> pd.DataFrame:
    """
    Preprocess data retrieved from Spotify API ready for analysis. 
    Cleaning includes dropping nulls and converting song duration from ms to mins.

    Args:
        - data (pd.DataFrame): dataframe of track IDs and audio features
    Returns
        - data (pd.DataFrame): cleaned dataframe
    """
    id_col = ['id']

    feature_cols = [
        'popularity',
        'danceability',
        'energy',
        'loudness',
        'mode',
        'speechiness',
        'acousticness',
        'instrumentalness',
        'liveness',
        'valence',
        'tempo',
        'duration_ms',
    ]
    
    data = data[id_col + feature_cols].copy()

    # drop rows where any of its values are null
    data.dropna(axis=0, how='any', inplace=True)

    # convert song duration from ms to mins
    data['duration_mins'] = data['duration_ms']/(1000*60)
    data.drop(columns='duration_ms', inplace=True)

    return data
