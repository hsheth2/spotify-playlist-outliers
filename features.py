import json
import spotipy
import os


def _fetch_tracks_from_playlist(sp, username, playlist_id):
    all_tracks = []
    results = sp.user_playlist(username, playlist_id, fields="tracks,next")

    tracks = results["tracks"]
    all_tracks += tracks["items"]
    while tracks["next"]:
        tracks = sp.next(tracks)
        all_tracks += tracks["items"]

    return [item["track"] for item in all_tracks]


def get_playlist(sp, username, playlist_id):
    tracks = _fetch_tracks_from_playlist(sp, username, playlist_id)

    uris = []
    for i, track in enumerate(tracks):
        print("   %d %32.32s %s" % (i, track["artists"][0]["name"], track["name"]))
        track_uri = track["uri"]
        uris.append(track_uri)

        # Force caching of these results.
        _ = get_audio_features(sp, track_uri)
        save_track_info(sp, track)

    return uris


def get_audio_features(sp: spotipy.client.Spotify, track_uri: str):
    track_uri = sp._get_id("track", track_uri)

    os.makedirs("audio_features", exist_ok=True)
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


def save_track_info(sp: spotipy.client.Spotify, track):
    track_uri = sp._get_id("track", track["uri"])

    os.makedirs("track_info", exist_ok=True)
    filename = f"track_info/{track_uri}"
    with open(filename, "w") as f:
        contents = json.dumps(track, indent=4)
        f.write(contents)


def get_track_info(sp: spotipy.client.Spotify, track_uri: str):
    track_uri = sp._get_id("track", track_uri)

    filename = f"track_info/{track_uri}"
    with open(filename, "r") as f:
        contents = f.read()
        track = json.loads(contents)
        return track
