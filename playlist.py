## THIS IS JUST A TEST FILE TO SEE IF I CAN GET THE GPT-3 API TO WORK WITH SPOTIFY PLAYLISTS

import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv, find_dotenv
import openai

class Config:

    def __init__(self):
        self.debug_mode               = os.environ.get('DEBUG_MODE')
        self.app_key                  = os.environ.get('APP_KEY')
        self.listen                   = os.environ.get('LISTEN')
        self.port                     = os.environ.get('PORT')
        self.spotify_client_id        = os.environ.get('SPOTIFY_CLIENT_ID')
        self.spotify_client_secret    = os.environ.get('SPOTIFY_CLIENT_SECRET')
        self.openai_api_key           = os.environ.get('OPENAI_API_KEY')

        # Tell our app where to get its environment variables from
        dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
        try:
            load_dotenv(dotenv_path)
        except IOError:
            find_dotenv()

class Playlist:
    def __init__(self, playlist_id):
        self.playlist_id = playlist_id

    def get_tracks(self):
        cfg = Config()
        # Authenticate with the Spotify API
        client_credentials_manager = SpotifyClientCredentials(client_id=cfg.spotify_client_id, client_secret=cfg.spotify_client_secret)
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

        # Get the tracks from the playlist
        results     = sp.playlist_items(self.playlist_id)
        tracks      = results['items']
        track_list  = []

        # Append the track name and artist to the list
        for track in tracks:
            track_list.append(track['track']['name'] + ' by ' + track['track']['album']['artists'][0]['name'])

        return track_list

class BlogPost:

    def __init__(self, playlist_id):
        self.playlist_id = playlist_id
    
    def generate_blog_post(self):
        # Authenticate with the OpenAI API
        openai.api_key = Config.openai_api_key
        
        playlist = Playlist(self.playlist_id)

        # Convert the playlist to a string
        playlist_to_str = '\n'.join(self.playlist)

        # Generate a blog post about the playlist
        prompt   = f"Write a blog post about the contents of this Spotify playlist in the style of a music blogger at Pitchfork:\n{playlist}"
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {'role': 'system', 'content': 'You are a chatbot'},
                {'role': 'user',   'content': prompt}
            ]
        )
        result = ''
        for choice in response.choices:
            result += choice.message.content

        try:
            return result
        except:
            return result

if __name__ == '__main__':
    playlist_id = '37i9dQZF1DXdPec7aLTmlC'
    playlist    = Playlist(playlist_id)
    blogpost    = BlogPost(playlist.get_tracks)
    print(playlist.get_tracks)
    print(type(blogpost.generate_blog_post))
    blogpost.generate_blog_post()