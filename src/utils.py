import pandas as pd 
from typing import List

def convert_json_to_df(data: List) -> pd.DataFrame:
    """
    Helper function to convert list of JSON response
    to pandas dataframe
    """

    return pd.json_normalize(data)

def split_into_batches(data: List, batch_size: int = 100) -> List:
    """
    Helper function to batch list into list of lists. This is 
    useful for src.api_requests.get_audio_feats_from_many_track_ids
    """
    
    return [data[i:i + batch_size] for i in range(0, len(data), batch_size)]

