import pandas as pd 
import matplotlib.pyplot as plt 
import numpy as np 
import seaborn as sns 

from typing import Tuple, List, Set

def plot_feature_dists(
        data: pd.DataFrame,
        feature_cols: List,
        n_rows: int = 3,
        n_cols: int = 4,
        figsize: Tuple = (12,8),
        ) -> None:
    """
    Function to plot histograms for each of the 12 audio features

    Args:
        - data (pd.DataFrame): dataframe of track IDs and audio features
        - feature_cols (List): audio features, e.g. popularity, danceability, energy
        - n_rows (int): number of rows of matplotlib subplots figure
        - n_cols (int): number of columns of matplotlib subplots figure
        - figsize (Tuple[int, int]): figsize of matplotlib final figure
    Returns:
        None
    """

    fig, axs = plt.subplots(n_rows, n_cols, figsize=figsize)
    feature_cols_reshaped = np.array(feature_cols).reshape(n_rows, n_cols)

    for i in range(n_rows):
        for j in range(n_cols):
            feature = feature_cols_reshaped[i,j]
            data[feature].plot.hist(bins=50, ax=axs[i,j])
            axs[i,j].set_title(feature)
    
    fig.tight_layout()

def calc_correlation(
        data: pd.DataFrame,
        feature_cols: List,
) -> pd.DataFrame:
    """
    Function to calculate Pearson correlation matrix for audio features

    Args:
        - data (pd.DataFrame): dataframe of track IDs and audio features
        - feature_cols (List): audio features, e.g. popularity, danceability, energy
    Returns:
        corr (pd.DataFrame): correlation matrix of audio features of shape (len(feature_cols), len(feature_cols))
    """

    corr = data[feature_cols].select_dtypes('number').corr()
    return corr

def plot_correlation(
        corr: pd.DataFrame,
        figsize: Tuple = (20,10),
        annot: bool = True,
) -> None:
    """
    Function to plot heatmap of correlation matrix

    Args:
        - corr (pd.DataFrame): correlation matrix of audio features
        - figsize (Tuple[int, int]): figsize of matplotlib final figure
        - annot (bool): whether to write correlation coefficients on plot
    Returns:
        None
    """
    plt.figure(figsize=figsize)
    sns.heatmap(corr, annot=annot)
    
def get_redundant_pairs(
        df: pd.DataFrame,
        ) -> Set[Tuple[str, str]]:
    """
    Function to get diagonal and lower triangular pairs of correlation matrix for eventual removal.
    Used in get_top_abs_correlations

    Args:
        - df (pd.DataFrame): dataframe of audio features
    Returns:
        - pairs_to_drop (Set): set of tuples of audio features from diagonal and lower triangle of correlation matrix
    """
    pairs_to_drop = set()
    cols = df.columns
    for i in range(0, df.shape[1]):
        for j in range(0, i+1):
            pairs_to_drop.add((cols[i], cols[j]))
    return pairs_to_drop

def get_top_abs_correlations(
        df: pd.DataFrame, 
        feature_cols: List[str], 
        n: int = 5,
        ) -> pd.DataFrame:
    """
    Function to get top n most strongly (absolute) correlated audio features.

    Args:
        - df (pd.DataFrame): dataframe of audio features
        - feature_cols (List[str]): audio feature columns
        - n (int): number of most correlated audio feature pairs to get
    Returns:
        - top_n (pd.Series): most correlated audio feature pairs and their absolute Pearson correlation coefficient.
    """
    df = df[feature_cols].select_dtypes('number')

    # calculate absolute correlation matrix
    au_corr = df.corr().abs().unstack()

    # get labels of audio feature pairs to remove (de-duplication)
    labels_to_drop = get_redundant_pairs(df)
    au_corr = au_corr.drop(labels=labels_to_drop).sort_values(ascending=False)
    
    # get top n audio feature pairs
    top_n = au_corr[:n]

    # flatten multiindex of series
    top_n.index = ['__'.join(feat) for feat in top_n.index.values]
    
    return top_n

