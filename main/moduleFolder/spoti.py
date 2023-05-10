#스포티파이
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth

class Spoti:

    def __init__(self):
        self.client_id = "baa750d0d8984735b51fa1c31b643d0b"
        self.client_secret = "42347bd6d3f8405188650673a3155594"
        self.client_credentials_manager = SpotifyClientCredentials(client_id=self.client_id, client_secret=self.client_secret)
        self.spotiInfo = spotipy.Spotify(client_credentials_manager=self.client_credentials_manager)

    def getSpotiData(self):
        return self.spotiInfo