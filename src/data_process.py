import pandas as pd 
import matplotlib.pyplot as plt 
import numpy as np 
import seaborn as sns 

from typing import Tuple

def preprocess_data(data: pd.DataFrame) -> pd.DataFrame:

    id_col = ['id']

    feature_cols = [
        'popularity',
        'danceability',
        'energy',
        # 'key',
        'loudness',
        'mode',
        'speechiness',
        'acousticness',
        'instrumentalness',
        'liveness',
        'valence',
        'tempo',
        'duration_ms',
        # 'time_signature',
    ]

    data = data[id_col + feature_cols].copy()

    data.dropna(axis=0, how='any', inplace=True)

    data['duration_ms'] = data['duration_ms']/(1000*60)

    data.rename(columns={'duration_ms': 'duration_mins'}, inplace=True)

    return data

def plot_feature_dists(
        data: pd.DataFrame,
        n_rows: int = 3,
        n_cols: int = 4,
        figsize: Tuple = (12,8),
        ):
    
    feature_cols = [
        'popularity',
        'danceability',
        'energy',
        # 'key',
        'loudness',
        'mode',
        'speechiness',
        'acousticness',
        'instrumentalness',
        'liveness',
        'valence',
        'tempo',
        'duration_mins',
        # 'time_signature',
    ]
    
    fig, axs = plt.subplots(n_rows, n_cols, figsize=figsize)
    feature_cols_reshaped = np.array(feature_cols).reshape(n_rows, n_cols)

    for i in range(n_rows):
        for j in range(n_cols):
            feature = feature_cols_reshaped[i,j]
            data[feature].plot.hist(bins=50, ax=axs[i,j])
            axs[i,j].set_title(feature)
    
    fig.tight_layout()
    
    return fig

def calc_correlation(
        data: pd.DataFrame,
) -> pd.DataFrame:
    
    feature_cols = [
        'popularity',
        'danceability',
        'energy',
        # 'key',
        'loudness',
        'mode',
        'speechiness',
        'acousticness',
        'instrumentalness',
        'liveness',
        'valence',
        'tempo',
        'duration_mins',
        # 'time_signature',
    ]

    corr = data[feature_cols].select_dtypes('number').corr()
    return corr

def plot_correlation(
        corr: pd.DataFrame,
        figsize: Tuple = (20,10),
        annot: bool = True,
):
    plt.figure(figsize=figsize)
    sns.heatmap(corr, annot=annot)
    
    