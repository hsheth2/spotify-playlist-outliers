import os
import spotipy
import spotipy.util
import dotenv
import pprint

import data

dotenv.load_dotenv()

scope = "user-library-read,playlist-read-private"

username = "hsheth2"

token = spotipy.util.prompt_for_user_token(username, scope)
if not token:
    print(f"Can't get token for {username}")
    exit(1)

sp = spotipy.Spotify(auth=token)


playlist_id = "https://open.spotify.com/playlist/3z91HHZMlFJsUZquZBbQnX"

uris = data.get_playlist(sp, username, playlist_id)

# print("   %d %32.32s %s" % (i, track["artists"][0]["name"], track["name"]))
# info = data.get_audio_features(sp, track)
# pprint.pprint(info)
