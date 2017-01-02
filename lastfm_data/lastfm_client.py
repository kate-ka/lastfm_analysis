import requests


class LastfmClient(object):
    def __init__(self):
        self.api_key = '33842f1efc79413ddc8affc6fbf8f755'
        self.api_url = 'http://ws.audioscrobbler.com/2.0/'

    def _prepare_params(self, **kwargs):
        params = {'api_key': self.api_key, 'format': 'json'}

        params.update(kwargs)

        return params

    def get_recent_tracks(self, username, page_from=1, page_to=None):
        params = self._prepare_params(method='user.getrecenttracks', user=username, limit=1000, page=1)

        current_page = page_from

        while True:
            params['page'] = current_page
            data = requests.get(self.api_url, params).json()
            last_page = int(data['recenttracks']['@attr']['totalPages'])

            page_tracks = []

            for track in data['recenttracks']['track']:
                if 'date' not in track:
                   continue

                page_tracks.append({
                    'artist': track['artist']['#text'],
                    'track': track['name'],
                    'album': track['album']['#text'],
                    'image': track['image'][2]['#text'],
                    'playback_date': track['date']['#text']
                })

            yield page_tracks

            if current_page == last_page:
                break

            if page_to and page_to == current_page:
                break

            current_page += 1

    def get_album(self, artist_name, album_name):
        params = self._prepare_params(method='album.getinfo', artist=artist_name, album=album_name)
        data = requests.get(self.api_url, params).json()

        if 'message' in data and data['message'] == 'Album not found':
            tracks_count = 0
        else:
            tracks_count = len(data['album']['tracks']['track'])
        if data['album']['image']:
            image_url = data['album']['image'][2]['#text']
        else:
            image_url = None

        return {
            'tracks_count': tracks_count,
            'image': image_url
        }


    # def count_album_tracks(self, album_name, artist_name):
    #     params = self._prepare_params(method='album.getinfo', artist=artist_name, album=album_name)
    #
    #     data = requests.get(self.api_url, params).json()
    #
    #     if 'message' in data and data['message'] == 'Album not found':
    #         tracks_count = 0
    #     else:
    #         tracks_count = len(data['album']['tracks']['track'])
    #
    #     return tracks_count
    #



