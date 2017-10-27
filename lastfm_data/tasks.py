from datetime import datetime
from uuid import uuid4

from time import time
from django.db.models.aggregates import Count
import requests
from django.core.files.base import ContentFile
from django.utils.encoding import smart_str
from . import lastfm_client
from lastfm_data.models import PlayedTrack, Artist, Album, ServiceUser, ArtistRate
from itertools import groupby
from math import sqrt


def fill_played_tracks(username, clearall=False, page_from=1, page_to=5):
    user = ServiceUser.objects.get(username=username)

    if clearall:
        d = PlayedTrack.objects.filter(user=user)
        d.delete()

    client = lastfm_client.LastfmClient()

    print('Handling page from {} to {} for {}'.format(page_from, page_to, username))
    t_start = time()

    pages = client.get_recent_tracks(username, page_from=page_from, page_to=page_to)

    played_tracks = []
    uids = set()

    artists_cache = {}

    album_cache = {}

    counter = 0
    for tracks in pages:
        t_end = time()
        print('Received tracks from lastfm for page from {} to {} for {}. time {}'.format(page_from, page_to, username,
                                                                                          t_end - t_start))
        t_start = time()

        for item in tracks:
            import hashlib

            # Get artist from cache or create if not exist
            if item['artist']:
                artist = artists_cache.get(item['artist'])

                if not artist:
                    artist, created = Artist.objects.get_or_create(name=item['artist'])
                    artists_cache[item['artist']] = artist
            else:
                artist = None

            # Get album from cache or create if not exist
            if item['album'] and artist:
                album = album_cache.get((item['artist'], item['album']))

                if not album:
                    image_url = item['image']
                    image = None
                    if image_url:
                        image = requests.get(image_url).content

                    album_data = client.get_album(artist.name, item['album'])
                    tracks_count = album_data['tracks_count']

                    album, created = Album.objects.get_or_create(
                        name=item['album'],
                        artist=artist,
                        tracks_count=tracks_count
                    )

                    if image:
                        album.image.save(image_url, ContentFile(image), save=True)

                    album_cache[(item['artist'], item['album'])] = album
            else:
                album = None

            uid = ':'.join((
                username,
                item['track'],
                item['artist'],
                item['album'] or '',
                str(datetime.strptime(item['playback_date'], "%d %b %Y, %H:%M" ))
            ))

            uid = hashlib.sha256(smart_str(uid).encode('utf-8')).hexdigest()

            if uid not in uids:
                uids.add(uid)
                model = PlayedTrack(
                    user=user,
                    track=item['track'],
                    artist=artist,
                    album=album,
                    playback_date=datetime.strptime(item['playback_date'], '%d %b %Y, %H:%M'),
                    uid=uid
                )

                played_tracks.append(model)
                counter += 1

            # Save data each 500 records
            if counter % 400 == 0:
                print ("saved %s tracks" % counter)
                PlayedTrack.objects.bulk_create(played_tracks)
                # Reset list for next 100 tracks
                played_tracks = []

        t_end = time()
        print('Created artists, albums, tracks for for page from {} to {} for {}. time {}'.format(
            page_from, page_to, username, t_end - t_start)
        )
        t_start = time()

    # Save the rest tracks for example when we have less 100 tracks
    # or 9545 tracks, in this case last 45 tracks will not be saved in for
    PlayedTrack.objects.bulk_create(played_tracks)
    print ("Done")


def create_and_get_artists(artists_name):
    """
    Gets or creates artists in bulk
    :param atist_name: list of artist name
    :return: dict like {
        "Metallica": <Artist: Metallica>,
        "Iron Maiden": <Artist: Iron Maiden>
    }
    """

    pass


def fill_track_new(user):
    client = lastfm_client.LastfmClient()
    # Get tracks from lastfm
    tracks = client.get_recent_tracks(user, pages=1)

    # Save data to models
    for track in tracks:
        if track['artist']:
            artist, created = Artist.objects.get_or_create(name=track['artist'])

            if track['album']:

                album, created = Album.objects.get_or_create(
                    name=track['album'],
                    artist=artist,
                    tracks_count=client.get_album(artist, track['album'])['tracks_count']
                )

                # Get image by url
                if track['image']:
                    response = requests.get(track['image'])
                    # Save image to image field
                    album.image.save(track['image'], ContentFile(response.content), save=True)

                PlayedTrack.objects.create(
                    user=user,
                    track=track['track'],
                    artist=artist,
                    album=album,
                    playback_date=datetime.strptime(track['playback_date'], '%d %b %Y, %H:%M'),
                    uid=str(uuid4())
                )


def update_album_model():

    albums = Album.objects.all()
    client = lastfm_client.LastfmClient()
    for album in albums:
        album.tracks_count = client.get_album(album.artist.name, album.name)['tracks_count']
        album.save()


def update_albums(username, update_images=True, update_tracks_count=True):
    if not username:
        albums = Album.objects.all()
    else:
        albums = Album.objects.filter(played_tracks__user=username).distinct()
    client = lastfm_client.LastfmClient()
    for album in albums:
        album_data = client.get_album(album.artist.name, album.name)
        if update_tracks_count:
            album.tracks_count = album_data['tracks_count']
        print (album_data['image'])
        if update_images and album_data['image']:
            image = requests.get(album_data['image']).content
            album.image.save(album_data['image'], ContentFile(image), save=True)

        album.save()


def fill_all_artist_rates():
    users = ServiceUser.objects.all()
    for user in users:
        fill_artist_rate(user)


def fill_artist_rate(user):
    artists_rates = Artist.objects.filter(playedtrack__user=user)\
        .values('name', 'id').annotate(played_count=Count('playedtrack'))\
        .order_by('-played_count')
    max_rates = artists_rates[0]['played_count']
    for artist_item in artists_rates:
        artist_rate = artist_item['played_count'] * 100 / max_rates
        ArtistRate.objects.create(
            user=user,
            artist_id=artist_item['id'],
            rate=artist_rate

        )

def prepre_rates():
    # raters = {}
    listeners = ArtistRate.objects.select_related('user', 'artist').values_list('user__username', 'artist__name',
                                                                                'rate')
    # for user, group in groupby(listeners, lambda item: item[0]):
    #     raters[user] = {artist: rate for __, artist, rate in list(group)}
    raters = {user: {artist: rate for __, artist, rate in list(group)} for user, group in groupby(listeners,
                                                                                                  lambda item: item[0])}

    return raters