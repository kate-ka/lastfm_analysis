import pylast

API_KEY = "33842f1efc79413ddc8affc6fbf8f755"
API_SECRET = "84ddcf8c1c79aeebbcec4a044fd031c9"


def get_lastfm_client():
    network = pylast.LastFMNetwork(api_key=API_KEY, api_secret=API_SECRET)
    return network


