import os
import spotipy
import spotipy.util
import dotenv
import pprint
import numpy as np

from pyod.models.knn import KNN
from pyod.models.lscp import LSCP
from pyod.models.pca import PCA

import data

dotenv.load_dotenv()

scope = "user-library-read,playlist-read-private"

username = "hsheth2"

token = spotipy.util.prompt_for_user_token(username, scope)
if not token:
    print(f"Can't get token for {username}")
    exit(1)

sp = spotipy.Spotify(auth=token)


def track_characteristics_array(sp: spotipy.client.Spotify, track_uri: str):
    # An example response from the API:
    """
    {'acousticness': 0.0422,
    'analysis_url': 'https://api.spotify.com/v1/audio-analysis/2cGxRwrMyEAp8dEbuZaVv6',
    'danceability': 0.775,
    'duration_ms': 337560,
    'energy': 0.585,
    'id': '2cGxRwrMyEAp8dEbuZaVv6',
    'instrumentalness': 0.619,
    'key': 10,
    'liveness': 0.077,
    'loudness': -9.516,
    'mode': 0,
    'speechiness': 0.0271,
    'tempo': 109.942,
    'time_signature': 4,
    'track_href': 'https://api.spotify.com/v1/tracks/2cGxRwrMyEAp8dEbuZaVv6',
    'type': 'audio_features',
    'uri': 'spotify:track:2cGxRwrMyEAp8dEbuZaVv6',
    'valence': 0.518}
    """

    characteristics = [
        'acousticness',
        'danceability',
        'duration_ms',
        'energy',
        'instrumentalness',
        #'key',  # Categorical: pitch class notation
        'liveness',
        'loudness',
        'mode',  # Categorical: major or minor
        'speechiness',
        'tempo',
        'time_signature',
        'valence',
    ]

    track = data.get_audio_features(sp, track_uri)

    values = [track[feature] for feature in characteristics]
    return values

# playlist_id = "https://open.spotify.com/playlist/3z91HHZMlFJsUZquZBbQnX"  # Harshal playlist
# playlist_id = "https://open.spotify.com/playlist/4yyfdbRQpx44MQwNPgBOek"  # No words playlist
playlist_id = "https://open.spotify.com/playlist/4DVTXRD4BzbjPSfbw1n74E"  # Questionable playlist
uris = data.get_playlist(sp, username, playlist_id)

# uri = 'spotify:track:2cGxRwrMyEAp8dEbuZaVv6'
# info = data.get_audio_features(sp, uri)
# values = track_characteristics_array(sp, uri)

X = np.array([track_characteristics_array(sp, track_uri) for track_uri in uris])

clf = PCA()
clf.fit(X)

ranks = sorted(zip(clf.decision_scores_, uris), reverse=True)
for score, track_uri in ranks:
    if score < clf.threshold_:
        break
    track = data.get_track_info(sp, track_uri)
    track_info = track_characteristics_array(sp, track_uri)
    prob = clf.predict_proba(np.array([track_info]), method="unify")[:,1][0]
    print("{: 12.3f} {: 6.3f} {:>32s} {:s}".format(score, prob, track["artists"][0]["name"], track["name"]))

