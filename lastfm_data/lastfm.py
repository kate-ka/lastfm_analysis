import os
from django.conf import settings
from itertools import groupby


def get_albums_by_months(username, with_image_path=False):
    """
    Get top albums for each year and month
    :param username: str
    :param with_image_path: bool Include image path in result or no
    :return: dict like {
        'top_albums': [{
            'year': 2016,
            'months': [
               {
                'month': 'March',
                'album': 'Mater of Puppets',
                'artist': 'Metallica',
                'img': 'http://img2-ak.lst.fm/i/u/770x0/e40b35d05f874c1da6fe052b91081c2f.jpg',
               },
               {
                   'month': 'February',
                   'album': 'Rust in Peace',
                   'artist': 'Megadeth',
                   'img': 'http://img2-ak.lst.fm/i/u/770x0/c48bdccaed704313c90d75a778db1afe.jpg',
               },
           ]
        },
        {
            'year': 2015,
            'months': [
                {
                    'month': 'May',
                    'album': 'Back to the Primitive',
                    'artist': 'Soulfly',
                    'img': 'http://img2-ak.lst.fm/i/u/174s/b1dbba72dcdc4f59b75a9df774dfc00f.jpg'
                },
                {
                    'month': 'June',
                    'album': 'Uncivillization',
                    'artist': 'Biohazard',
                    'img': 'http://img2-ak.lst.fm/i/u/300x300/20e5b14cbb66428c936b52ac2178aab0.jpg'
                }
            ]
        }]
    }
    """

    from lastfm_data.models import PlayedTrack
    from django.db.models.aggregates import Count

    tracks = (
        PlayedTrack.objects
        .filter(user__username=username)
        .extra(select={
            'played_year': "DATE_PART('year', lastfm_data_playedtrack.playback_date)",
            'played_month': "DATE_PART('month', lastfm_data_playedtrack.playback_date)",
        })
        .values('played_year', 'played_month', 'album__name', 'artist__name', 'album__image')
        .annotate(tracks_count=Count('*'))
        .order_by('-played_year', '-played_month', '-tracks_count'))

    result = {
        'top_albums': []
    }

    for year, grouped_by_year in groupby(tracks, lambda x: x['played_year']):
        result_year = {'year': year, 'months': []}

        for month, grouped_by_month in groupby(list(grouped_by_year), lambda x: x['played_month']):
            group = list(grouped_by_month)[0]

            image_url = None
            image_path = None

            if group['album__image']:
                image_url = settings.MEDIA_URL + group['album__image']
                if with_image_path:
                    image_path = os.path.join(settings.MEDIA_ROOT, group['album__image'])

            result_year['months'].append({
                'month': month,
                'album': group['album__name'],
                'artist': group['artist__name'],
                'img': image_url,
                'image_path': image_path
            })

        result['top_albums'].append(result_year)

    return result


def get_my_scrobles_generator():
    import requests
    params = {"method":"user.getrecenttracks", "user": "metalpumpkin", "api_key": "33842f1efc79413ddc8affc6fbf8f755",
              "limit":10, "page":1, "format": "json"}
    url= "http://ws.audioscrobbler.com/2.0/"
    current_page = 1
    while True:
        params['page'] = current_page
        data = requests.get(url, params=params).json()
        last_page = int(data['recenttracks']['@attr']['totalPages'])
        if current_page == 10:
            break
        for track in data['recenttracks']['track']:
            yield track
        current_page += 1


def counter(items, get_key):
    counted = {}
    for item in items:
        key_item = get_key(item)

        counted[key_item] = counted.get(key_item, 0) + 1
    return counted


def group_by_user(item):
    return item['user']


def group_by_album(item):
    return item['album']

