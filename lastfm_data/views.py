from PIL.Image import Image
from datetime import datetime, timedelta
from django.db.models.aggregates import Count
from django.http.response import JsonResponse, HttpResponse
from django.shortcuts import render
from lastfm_data.lastfm import get_albums_by_months
from utils import lastfm_client
from lastfm_data.models import PlayedTrack, Album, Artist, ServiceUser
from lastfm_data.tasks import fill_played_tracks, topMatches, prepre_rates, \
    sim_pearson, sim_distance, getRecommendations
import logging

logger = logging.getLogger('lastfm')


def lastfm_get_top_artists(request, username):
    # client = lastfm_client.get_lastfm_client()
    # lastfm_user = client.get_user(username)
    # artists = lastfm_user.get_top_artists()
    # lastfm_artists = []
    # for artist in artists:
    #     lastfm_artists.append(
    #         {'name': artist.item.name,
    #          'plays': artist.weight}
    #     )

    if not ServiceUser.objects.filter(username=username).exists():
        fill_played_tracks(username)

    top_artists = ServiceUser.objects.filter(username=username).get_top_artists()
    items = {'artists': top_artists}

    return JsonResponse(data=items)



def index(request):
    # find_sim_pearson('metallist-ka')
    # topMatches(prepre_rates(), 'metallist-ka', n=7, similarity=sim_distance)
    return render(request, 'lastfm_data/index.html')


def load_data(request, username):
    # raise Exception(username)

    if PlayedTrack.objects.filter(user=username).exists():
        return JsonResponse({'success':True})
    else:
        try:
            fill_played_tracks(username, None, False)
            return JsonResponse({'success': True})
        except Exception, e:
            raise
            logger.error('Failed to load data from lastfm: %s' % e)
            return JsonResponse({'success': False})



def getall_scrobbles_by_year(request, username):
    scrobbles_by_year = PlayedTrack.objects.get_scrobbles_by_year(username=username)

    # [(2009, 1896), (2010, 704), (2011, 464), (2012, 419), (2013, 233), (2014, 779), (2015, 447)]
    scrobbles = []
    for scrobble in scrobbles_by_year:
        scrobbles.append(
            {'year': scrobble[0],
             'scrobbles': scrobble[1]}
        )
    items = {'scrobbles': sorted(scrobbles, key=lambda item: item['year'])}

    return JsonResponse(data=items)


def get_top_albums_by_years(request, username):
    """
    Get top album for each year and month.

    Returns json like this: {
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

    :param request: HttpRequest object
    :param username: str
    :return: HttpResponse
    """
    from lastfm_data import lastfm

    data = lastfm.get_albums_by_months(username)
    # data = {'top_albums': sorted(d['top_albums'], key=lambda item: item['year'])}
    return JsonResponse(data=data)


def get_photo_collage(request, username):
    # data = get_albums_by_months(username, with_image_path=True)
    d = get_albums_by_months(username, with_image_path=True)
    data = {'top_albums': sorted(d['top_albums'], key=lambda item: item['year'], reverse=True)}
    # print(data)
    images = []
    for item in data['top_albums']:
        if len(images) == 12:
            break
        for album in item['months']:
            # print album
            if album['img']:
                # print album['image_path']

                images.append(album['image_path'])
            if len(images) == 12:
                break

    from PIL import Image
    result = Image.new("RGB", (696, 522))

    #
    # coords = []
    # for y in range(0, 522, 174):
    #     for x in range(0, 696, 174):
    #         coords.append((x, y))
    #
    # for i in range(len(coords)-1):
    #     x = coords[i][0]
    #     y = coords[i][1]
    #     img = Image.open(images[i])
    #     img.thumbnail((174, 174), Image.ANTIALIAS)
    #     w, h = img.size
    #     print('pos {0},{1} size {2},{3}'.format(x, y, w, h))
    #     result.paste(img, (x, y, x + w, y + h))
    # result.save('collage.jpg')
    #
    # try:
    #     with open('collage.jpg', "rb") as f:
    #         return HttpResponse(f.read(), content_type="collage/jpeg")
    # except IOError:
    #     response = HttpResponse(content_type="collage/jpeg")
    #     result.save(response, "JPEG")
    # return response


    coords = []
    y = 0
    x = 0
    for i in range(1,14):
        coords.append((x, y))
        x += 174
        if not i % 4:
            x = 0
            y += 174
    for image, cords in list(zip(images, coords)):
        x = cords[0]
        y = cords[1]
        img = Image.open(image)
        img.thumbnail((174, 174), Image.ANTIALIAS)
        w, h = img.size
        # print('pos {0},{1} size {2},{3}'.format(x, y, w, h))
        result.paste(img, (x, y, x + w, y + h))
    result.save('media/collage.jpg')
    try:
        with open('media/collage.jpg', "rb") as f:
            return HttpResponse(f.read(), content_type="collage/jpeg")
    except IOError:
        response = HttpResponse(content_type="collage/jpeg")
        result.save(response, "JPEG")
    return response


def get_forgotten_albums(request, username):
    half_year_ago_date = datetime.now() - timedelta(days=180)
    from_date = request.GET['from_date']
    old_albums = (
        PlayedTrack.objects
        .filter(
            playback_date__lt=half_year_ago_date,
            playback_date__year__gte=from_date,
            album__isnull=False,
            user__username=username)
        .values('artist', 'album', 'artist__name', 'album__name')
        .annotate(count=Count('*'))
        .order_by('artist', 'album')
    )
    forgotten_albums = []
    for old_album in old_albums:
        album = Album.objects.get(id=old_album['album'], artist_id=old_album['artist'])
        if album.image:
            old_album['image'] = album.image.url
        else:
            old_album['image'] = None
        tracks_count = album.tracks_count
        tracks = PlayedTrack.objects.filter(album=old_album['album'], user__username=username).order_by('-playback_date')
        old_album['last_listened'] = tracks[0].playback_date.year

        is_listened_last_six_month = PlayedTrack.objects.filter(
            user__username=username, playback_date__gte=half_year_ago_date, album=album).exists()

        if not is_listened_last_six_month and tracks_count > 0 and old_album['count'] / tracks_count > 2:
            forgotten_albums.append({
                'album_image': old_album['image'],
                'artist': old_album['artist__name'],
                'album': old_album['album__name'],
                'last_listened': old_album['last_listened'],
                'total_scrobbles': old_album['count']
            })

    items = { 'forgotten_albums': sorted(forgotten_albums, key=lambda item: item['total_scrobbles'], reverse=True)}
    # items = {
    #     'forgotten_albums':
    #         [
    #               {
    #                   'album_image': 'http://127.0.0.1:8000/media/album_images/0a5fa3d617f246548af137271fc68ada_BVr3E2i.png',
    #                   'artist': 'Metallica',
    #                   'album': 'Master of Puppets',
    #                   'last_listened': 2012,
    #                   'total_scrobbles': 5
    #               },
    #             {
    #                 'album_image': 'http://127.0.0.1:8000/media/album_images/0a40013700274522b45dc90148b665bf_bL1HqBy.png',
    #                   'artist': 'Murtalica',
    #                   'album': 'Tralala',
    #                   'last_listened': 2011,
    #                   'total_scrobbles': 50
    #               },
    #             {
    #                 'album_image': 'http://127.0.0.1:8000/media/album_images/3fb805c77cb645d0aaac2514e025fcfe_Z2FxHi4.png',
    #                   'artist': 'MickyMouse',
    #                   'album': 'Of Mice And Men',
    #                   'last_listened': 2014,
    #                   'total_scrobbles': 23
    #               }
    #         ]
    # }

    return JsonResponse(data=items)

