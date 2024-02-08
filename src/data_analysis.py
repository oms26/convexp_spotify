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

    corr = data[feature_cols].select_dtypes('number').corr()
    return corr

def plot_correlation(
        corr: pd.DataFrame,
        figsize: Tuple = (20,10),
        annot: bool = True,
) -> None:
    plt.figure(figsize=figsize)
    sns.heatmap(corr, annot=annot)
    
def get_redundant_pairs(df: pd.DataFrame) -> Set[Tuple[str, str]]:
    '''Get diagonal and lower triangular pairs of correlation matrix'''
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
    df = df[feature_cols].select_dtypes('number')
    au_corr = df.corr().abs().unstack()
    labels_to_drop = get_redundant_pairs(df)
    au_corr = au_corr.drop(labels=labels_to_drop).sort_values(ascending=False)
    top_n = au_corr[:n]
    top_n.index = ['__'.join(feat) for feat in top_n.index.values]
    return top_n