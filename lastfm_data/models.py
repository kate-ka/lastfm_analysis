#coding=utf-8
from __future__ import unicode_literals

from django.db import models
from django.db.models.aggregates import Count


class PlayedTrackQueryset(models.QuerySet):
    def get_scrobbles_by_year(self, username):
        played_tracks = self.filter(user__username=username)
        from collections import defaultdict

        dd = defaultdict(int)
        for track in played_tracks:
            dd[track.playback_date.year] += 1
        return list(dd.items())


class ServiceUserQueryset(models.QuerySet):
    def get_top_artists(self):
        artists = (
            PlayedTrack.objects
            .filter(user__in=self)
            .values('user__username', 'artist__name')
            .annotate(count_artist=Count('artist'))
            .order_by('-count_artist')
        )[:10]
        top_artists = []
        for artist in artists:
            top_artists.append({
                "name": artist['artist__name'],
                "plays": artist['count_artist']
            })
        return top_artists

# pt = PlayedTrack.objects.get_scrobbles_by_year('metallist-ka')

#[(2009, 1896), (2010, 704), (2011, 464), (2012, 419), (2013, 233), (2014, 779), (2015, 447)]

# s = {}
# >>> for item in d:
# ...     if item.playback_date.year not in s:
# ...         s[item.playback_date.year] = 0
# ...     s[item.playback_date.year] = s[item.playback_date.year] + 1


# pusto = {}
# >>> for track in d:
# ...     key = track.playback_date.year
# ...     pusto[key] = pusto.setdefault(key, 0) + 1
# ...
# >>> pusto
# {2009: 1896, 2010: 704, 2011: 464, 2012: 419, 2013: 233, 2014: 779, 2015: 447}
# >>>

#  from collections import Counter
# >>> years = [x.playback_date.year for x in d]
# >>> frg = Counter(years)
# >>> frg
# Counter({2009: 1896, 2014: 779, 2010: 704, 2011: 464, 2015: 447, 2012: 419, 2013: 233})

# data = {
#     year: len(list(group))
#     for year, group in groupby(
#         played_tracks,
#         lambda track: track.playback_date.year)
# }

#     PlayedTrack.objects.extra(select={'year': "DATE_PART('year', lastfm_data_playedtrack.playback_date)"})\
#         .values('year').annotate(tracks_count=Count('id')).order_by('year')
# [{'tracks_count': 949, 'year': 2009.0}, {'tracks_count': 704, 'year': 2010.0},
#  {'tracks_count': 464, 'year': 2011.0}, {'tracks_count': 419, 'year': 2012.0},
#  {'tracks_count': 233, 'year': 2013.0}, {'tracks_count': 779, 'year': 2014.0},
#  {'tracks_count': 447, 'year': 2015.0}, {'tracks_count': 4, 'year': 2016.0}]

class Artist(models.Model):
    name = models.CharField(null=True, max_length=256)

    def __unicode__(self):
        return unicode(self.name)


class Album(models.Model):
    name = models.CharField(null=True, blank=True, max_length=256)
    tracks_count = models.PositiveSmallIntegerField(null=True)
    artist = models.ForeignKey(Artist)
    image = models.ImageField(upload_to='album_images', null=True, blank=True)

    def __unicode__(self):
        return unicode(self.name)


class PlayedTrack(models.Model):
    user = models.ForeignKey('lastfm_data.ServiceUser', null=True, blank=True)
    artist = models.ForeignKey(Artist, null=True, blank=True)
    track = models.CharField(null=True, blank=True, max_length=256)
    playback_date = models.DateTimeField()
    album = models.ForeignKey(Album, blank=True, null=True, related_name='played_tracks')
    uid = models.CharField(max_length=256, unique=True)
    objects = PlayedTrackQueryset.as_manager()

    def __unicode__(self):
        return unicode(self.track)


class ArtistRate(models.Model):
    user = models.ForeignKey('lastfm_data.ServiceUser', null=True, blank=True)
    artist = models.ForeignKey(Artist, null=True, blank=True)
    rate = models.PositiveSmallIntegerField(null=True)


class ServiceUser(models.Model):
    username = models.CharField(null=True, blank=True, max_length=256)
    objects = ServiceUserQueryset.as_manager()

    def __unicode__(self):
        return unicode(self.username)


