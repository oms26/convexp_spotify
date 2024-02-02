
from dotenv import load_dotenv 
import os

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")

token_endpoint_url = "https://accounts.spotify.com/api/token"
base_url = "https://api.spotify.com/v1"


