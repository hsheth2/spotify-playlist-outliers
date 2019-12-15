import os
import spotipy
import spotipy.util
import dotenv
import pprint

import features

dotenv.load_dotenv()

scope = "user-library-read,playlist-read-private"

username = "hsheth2"

token = spotipy.util.prompt_for_user_token(username, scope)
if not token:
    print(f"Can't get token for {username}")
    exit(1)

sp = spotipy.Spotify(auth=token)


def fetch_tracks_from_playlist(sp, username, playlist_id):
    all_tracks = []
    results = sp.user_playlist(username, playlist_id, fields="tracks,next")

    tracks = results["tracks"]
    all_tracks += tracks["items"]
    while tracks["next"]:
        tracks = sp.next(tracks)
        all_tracks += tracks["items"]

    return [item["track"] for item in all_tracks]


def show_tracks(tracks):
    for i, track in enumerate(tracks):
        print("   %d %32.32s %s" % (i, track["artists"][0]["name"], track["name"]))


playlist_id = (
    "https://open.spotify.com/playlist/3z91HHZMlFJsUZquZBbQnX"
)

tracks = fetch_tracks_from_playlist(sp, username, playlist_id)
show_tracks(tracks)
pprint.pprint(tracks[0])

# info = features.get_audio_features(sp, track)
# pprint.pprint(info)
