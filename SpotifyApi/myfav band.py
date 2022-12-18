
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

the1975 = 'spotify:artist:3mIj9lX2MWuHmhNCA7LSCW'
#correct way of auth without using env variable
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id='8f5eec7ea6e243c9a41c8be9b372158d', client_secret='719fbd166290401d96c88f7a1ffcf8ce'))
results = spotify.artist_top_tracks(the1975)

for track in results ['tracks'][:10]:
    print('track    : ' + track['name'])
    print('cover art: ' + track['album']['images'][0]['url'])
    print()