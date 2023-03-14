import os
import openai
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv, find_dotenv

class Config:

    def __init__(self):
        self.debug_mode               = os.environ.get('DEBUG_MODE')
        self.app_key                  = os.environ.get('APP_KEY')
        self.listen                   = os.environ.get('LISTEN')
        self.port                     = os.environ.get('PORT')
        self.spotify_client_id        = os.environ.get('SPOTIFY_CLIENT_ID')
        self.spotify_client_secret    = os.environ.get('SPOTIFY_CLIENT_SECRET')
        self.openai_api_key           = os.environ.get('REMOTE_QUESTION_WORDLIST')

        # Tell our app where to get its environment variables from
        dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
        try:
            load_dotenv(dotenv_path)
        except IOError:
            find_dotenv()

class Playlist:

    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self.tracks = self.get_tracks()

    def get_tracks(self):
        # Authenticate with the Spotify API
        client_credentials_manager = SpotifyClientCredentials(client_id=Config.spotify_client_id, client_secret=Config.spotify_client_secret)
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

        # Get the tracks from the playlist
        results = sp.playlist_items(self.playlist_id)
        tracks = results['items']

        return tracks
    
    def get_track_names(self):
        track_names = []
        for track in self.tracks:
            track_names.append(track['track']['name'])
        return track_names
    
    def get_track_artists(self):
        track_artists = []
        for track in self.tracks:
            track_artists.append(track['track']['artists'][0]['name'])
        return track_artists
    
    def get_track_albums(self):
        track_albums = []
        for track in self.tracks:
            track_albums.append(track['track']['album']['name'])
        return track_albums
    
class BlogPost:

    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
        self.playlist    = Playlist(self.playlist_id)
        self.blog_post   = self.generate_blog_post()
    
    def generate_blog_post(self):
        # Authenticate with the OpenAI API
        openai.api_key = Config.openai_api_key
        
        # Generate a blog post about the playlist
        prompt = f"Write a blog post about the contents of this Spotify playlist:\n{self.playlist.get_track_names()}"
        response = openai.Completion.create(
            engine="davinci",
            prompt=prompt,
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.7,
        )
        blog_post = response.choices[0].text
        return blog_post