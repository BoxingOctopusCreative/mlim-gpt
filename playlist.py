import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Enter your client ID and client secret here
client_id = "your_client_id"
client_secret = "your_client_secret"

# Authenticate with the Spotify API
client_credentials_manager = SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Enter the playlist ID here
playlist_id = "your_playlist_id"

# Get the tracks from the playlist
results = sp.playlist_items(playlist_id)
tracks = results['items']

# Print the names of the tracks
for track in tracks:
    print(track['track']['name'])
