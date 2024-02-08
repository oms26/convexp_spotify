import json
import pandas as pd 
import requests 
import base64
from typing import List

from src.constants import CLIENT_ID, CLIENT_SECRET, token_endpoint_url, base_url
from src.utils import convert_json_to_df

class SpotifyService:
    """
    Class holding functions for sending HTTP requests to Spotify Web API. 
    Functions include retrieving an artist's songs and their audio features.
    """
    def __init__(self):
        """
        Attributes:
            self.token: access token for Spotify API access
            self.headers: authorisation header to authorise HTTP requests
        """

        auth_string = CLIENT_ID + ":" + CLIENT_SECRET
        auth_bytes = auth_string.encode("utf-8")
        auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

        headers = {
            "Authorization": "Basic " + auth_base64,
            "Content-Type": "application/x-www-form-urlencoded"
        }

        data = {
            "grant_type": "client_credentials"
        }

        auth_response = requests.post(
            url=token_endpoint_url,
            headers=headers,
            data=data,
            verify=False # bypass SSL certificate verification for local throwaway app
        )

        response_dict = json.loads(auth_response.content)

        self.token = response_dict["access_token"]
        self.headers = {"Authorization": "Bearer " + self.token}

    def get_songs_from_artist_name(
            self, 
            artist_name: str,
            ) -> pd.Series:
        """
        Function to query search endpoint for songs from chosen artist

        Args:
            - artist_name (str): Name of artist to get songs from.
        Returns:
            - s_tracks (pd.Series): track IDs of all artist's tracks
        """
        params = {
            'q': f"artist:{artist_name}",
            'type': 'track',
        }

        search_endpoint_url = base_url + "/search"

        track_ids = []
        
        # as each request gives only one page of track results, loop through all pages to get all songs
        while search_endpoint_url:
            
            response = requests.get(search_endpoint_url, params=params, headers=self.headers, verify=False)
            response_dict = json.loads(response.content)
            for item in response_dict["tracks"]["items"]:
                track_id = item['id']
                track_ids.append(track_id)
            search_endpoint_url = response_dict["tracks"]['next']
            params = {} # reinitialise query params to empty dict, as full query URL given in 'next' key

        track_ids = list(set(track_ids))
        s_tracks = pd.Series(track_ids, name='id')
        
        return s_tracks
    
    def get_audio_feats_from_track_id(
            self, 
            track_id: str,
            ) -> pd.DataFrame:
        """
        Function to get audio features from a single track ID endpoint.

        Args:
            - track_id (str): ID of track
        Returns:
            - audio_features_df (pd.DataFrame): dataframe of single track ID and features including popularity, danceability, etc.
        """
        
        query_url = base_url + f"/audio-features/{track_id}"
        response = requests.get(
            url=query_url,
            headers=self.headers,
            verify=False,
        )
        audio_features = json.loads(response.content)

        audio_features_df = convert_json_to_df(audio_features)

        return audio_features_df
    
    def get_audio_feats_from_many_track_ids(
            self, 
            track_ids: List[str],
            ) -> pd.DataFrame:
        """
        Function to send GET request for audio features from a list of track IDs.
        Same functionality as get_audio_feats_from_track_id but only needs to send single request for many songs.
        This function is called by get_audio_feats_full

        Args:
            - track_ids (List[str]): IDs of several tracks
        Returns:
            - audio_features_df (pd.DataFrame): dataframe of several track IDs and features including popularity, danceability, etc.
        """

        query_url = base_url + f"/audio-features"

        ids_query = ",".join(track_ids)
        params = {
            "ids": ids_query,
        }

        response = requests.get(
            url=query_url,
            params=params,
            headers=self.headers,
            verify=False,
        )
        features_dict = json.loads(response.content)
        audio_features = features_dict['audio_features']

        audio_features_df = convert_json_to_df(audio_features)

        return audio_features_df
    
    def get_audio_feats_full(
            self, 
            batches: List,
            ) -> pd.DataFrame:
        """
        Function to get audio features from a list of list of track IDs.
        Performs GET requests by calling get_audio_feats_from_many_track_ids

        Args:
            - batches (List): nested list of track IDs of all artist's tracks
        Returns:
            - audio_features_df (pd.DataFrame): dataframe of all artist's track IDs and features including popularity, danceability, etc.
        """
        
        df_list = []
        for batch in batches:
            batch_df = self.get_audio_feats_from_many_track_ids(batch)
            df_list.append(batch_df)

        audio_features_df = pd.concat(df_list)

        return audio_features_df
    
    def get_popularity_from_track_id(
            self, 
            track_id: str,
            ) -> int:
        """
        Function to get popularity from a single track ID.

        Args:
            - track_id (str): ID of track
        Returns:
            - popularity (int): popularity of song
        """
        
        query_url = base_url + f'/tracks/{track_id}'

        response = requests.get(
            url=query_url,
            headers=self.headers,
            verify=False,
        )

        response_dict = json.loads(response.content)
        popularity = response_dict['popularity']

        return popularity
        
