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
        self.tracks      = self.get_tracks()

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

    def __init__(self, playlist_id, openai_api_key):
        self.playlist_id = playlist_id
        self.openai_api_key = openai_api_key
        self.playlist    = Playlist(self.playlist_id)
        self.blog_post   = self.generate_blog_post()
    
    def generate_blog_post(self):
        # Authenticate with the OpenAI API
        openai.api_key = Config.openai_api_key
        
        # Generate a blog post about the playlist
        prompt   = f"Write a blog post about the contents of this Spotify playlist in the style of a music blogger at Pitchfork:\n{self.playlist}"
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
            return str(type(result))

class SwaggerDef:

    def __init__(self):
        self.template = {
            #"host":            "https://chainsinventinsanity.com",  # overrides localhost:500
            "swagger":        "2.0",
            "swagger_ui_css": "https://raw.githubusercontent.com/Amoenus/SwaggerDark/master/SwaggerDark.css",
            "termsOfService": "https://api.mylifeinmusic.com/terms",
            "version":        "2.0",
            "basePath":       "/",  # base bash for blueprint registration
            "operationId":    "getmyData",
            "schemes":         ["http", "https"],
            "info": {
                "title":       "MLIM GPT API",
                "description": "API for My Life in Music Blog Post Generator",
                "contact":      {
                    "responsibleOrganization": "Boxing Octopus Creative",
                    "responsibleDeveloper":    "ryan.draga@boxingoctop.us",
                    "email":                   "ryan.draga@boxingoctop.us",
                    "url":                     "https://boxingoctop.us",
                }
            }
        }

        self.swagger_config = {
            #"static_url_path":                "/flasgger_static",
            #"static_folder":                  "static",  # must be set by user
            "swagger_ui":                      True,
            "specs_route":                     "/apidocs/",
            "favicon":                         "https://chains-invent-insanity-assets.sfo3.digitaloceanspaces.com/images/swagger_fav.png",
            "swagger_ui_bundle_js":            'https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/4.5.0/swagger-ui-bundle.js',
            "swagger_ui_standalone_preset_js": 'https://cdnjs.cloudflare.com/ajax/libs/swagger-ui/4.5.0/swagger-ui-standalone-preset.js',
            'jquery_js':                       'https://cdnjs.cloudflare.com/ajax/libs/jquery/3.6.0/jquery.min.js',
            'swagger_ui_css':                  'https://chains-invent-insanity-assets.sfo3.digitaloceanspaces.com/css/theme-newspaper.css',
            "headers":                          [],
            "specs":                            [
                {
                    "endpoint":     'apispec_1',
                    "route":        '/apispec_1.json',
                    "rule_filter":  lambda rule: True,  # all in
                    "model_filter": lambda tag: True,  # all in
                }
            ],
        }