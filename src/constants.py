from dotenv import load_dotenv 
import os

load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")

token_endpoint_url = "https://accounts.spotify.com/api/token"
base_url = "https://api.spotify.com/v1"


