import pandas as pd 
from typing import List

def preprocess_data(
        data: pd.DataFrame,
        ) -> pd.DataFrame:

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

    data.dropna(axis=0, how='any', inplace=True)

    data['duration_mins'] = data['duration_ms']/(1000*60)

    data.drop(columns='duration_ms', inplace=True)

    return data
