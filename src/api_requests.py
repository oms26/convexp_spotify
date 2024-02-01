import os
import json
import numpy as np 
import pandas as pd 
import requests 
import base64
from typing import Dict, List, Tuple

from src.constants import client_id, client_secret, token_endpoint_url, base_url
from src.utils import convert_json_to_df

class SpotifyService:
    def __init__(self):
        auth_string = client_id + ":" + client_secret
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

    def get_songs_from_artist_name(self, artist_name: str) -> pd.DataFrame:

        params = {
            'q': f"artist:{artist_name}",
            'type': 'track',
        }

        search_endpoint_url = base_url + "/search"

        track_ids = []
        track_names = []
        while search_endpoint_url:
            
            response = requests.get(search_endpoint_url, params=params, headers=self.headers, verify=False)
            response_dict = json.loads(response.content)
            for item in response_dict["tracks"]["items"]:
                track_id = item['id']
                track_ids.append(track_id)
                track_name = item['name']
                track_names.append(track_name)
            search_endpoint_url = response_dict["tracks"]['next']
            params = {} # reinitialise query params to empty dict, as full query URL given in 'next' key

        df_tracks = pd.DataFrame({
            'track_id': track_ids,
            'track_name': track_names,
        })
        
        return df_tracks
    
    def get_audio_feats_from_track_id(self, track_id: str) -> pd.DataFrame:
        query_url = base_url + f"/audio-features/{track_id}"
        response = requests.get(
            url=query_url,
            headers=self.headers,
            verify=False,
        )
        audio_features = json.loads(response.content)

        audio_features_df = convert_json_to_df(audio_features)

        return audio_features_df
    
    def get_audio_feats_from_many_track_ids(self, track_ids: List) -> pd.DataFrame:

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
        
####################### NOT USED CURRENTLY ##############################
    
    def get_artist_id_from_name(self, artist_name: str) -> str:

        params = {
            'q': artist_name,
            'type': 'artist',
            'limit': 1
        }

        search_endpoint_url = base_url + "/search"

        response = requests.get(
            url=search_endpoint_url,
            params=params,
            headers=self.headers,
            verify=False,
        )

        response_dict = json.loads(response.content)
        artist_items = response_dict["artists"]["items"]

        if not artist_items:
            print(f"Artist with name: {artist_name} does not exist...")
            artist_id = None
        else:
            artist = artist_items[0]
            artist_id = artist["id"]

        return artist_id
    
    def get_album_ids_from_artist_id(self, artist_id: str, limit: int = 50) -> List:

        params = {
            "include_groups": "album,single",
            "limit": limit,
        }

        artists_endpoint_url = base_url + "/artists"
        query_url = artists_endpoint_url + f'/{artist_id}/albums'

        response = requests.get(
            url=query_url,
            params=params,
            headers=self.headers,
            verify=False,
        ) 

        response_dict = json.loads(response.content)

        album_ids = [album['id'] for album in response_dict['items']]

        return album_ids
    
    def get_song_ids_from_album_id(self, album_id: str, limit: int = 50) -> List:
        albums_endpoint_url = base_url + "/albums"
        query_url = albums_endpoint_url + f"/{album_id}/tracks"

        params = {
            'limit': limit
        }

        response = requests.get(
            url=query_url,
            params=params,
            headers=self.headers,
            verify=False,
        ) 

        response_dict = json.loads(response.content)

        song_ids = [song['id'] for song in response_dict['items']]

        return song_ids
    







    def get_top_tracks_from_artist_id(self, artist_id: str) -> pd.DataFrame:
        """
        This request can be used in initial summary of artist
        """
        artists_endpoint_url = base_url + "/artists"
        query_url = artists_endpoint_url + f'/{artist_id}/top-tracks'

        params = {
            'market': 'US',
        }

        response = requests.get(
            url=query_url,
            params=params,
            headers=self.headers,
            verify=False,
        ) 

        response_dict = json.loads(response.content)

        top_tracks_list = [(track['name'], track['album']['name'], track['popularity']) for track in response_dict['tracks']]
        top_tracks_df = pd.DataFrame(top_tracks_list, columns=['track_title', 'album_title', 'popularity'])

        return top_tracks_df






