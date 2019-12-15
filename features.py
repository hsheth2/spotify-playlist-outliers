import json
import spotipy
import os


def get_audio_features(sp: spotipy.client.Spotify, track_uri: str):
    track_uri = sp._get_id("track", track_uri)

    os.mkdir("audio_features")
    filename = f"audio_features/{track_uri}"
    try:
        with open(filename, "r") as f:
            contents = f.read()
            data = json.loads(contents)
    except FileNotFoundError:
        features = sp.audio_features([track_uri])
        data = features[0]
        with open(filename, "w") as f:
            contents = json.dumps(data, indent=4)
            f.write(contents)
    return data
