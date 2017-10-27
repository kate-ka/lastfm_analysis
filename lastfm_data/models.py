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


class Artist(models.Model):
    name = models.CharField(null=True, max_length=256, unique=True)

    def __str__(self):
        return self.name


class Album(models.Model):
    name = models.CharField(null=True, blank=True, max_length=256)
    tracks_count = models.PositiveSmallIntegerField(null=True)
    artist = models.ForeignKey(Artist)
    image = models.ImageField(upload_to='album_images', null=True, blank=True)

    class Meta:
        unique_together = (('name', 'artist'),)

    def __str__(self):
        return self.name


class PlayedTrack(models.Model):
    user = models.ForeignKey('lastfm_data.ServiceUser', null=True, blank=True)
    artist = models.ForeignKey(Artist, null=True, blank=True)
    track = models.CharField(null=True, blank=True, max_length=256)
    playback_date = models.DateTimeField()
    album = models.ForeignKey(Album, blank=True, null=True, related_name='played_tracks')
    uid = models.CharField(max_length=256, unique=True)
    objects = PlayedTrackQueryset.as_manager()

    def __str__(self):
        return self.track


class ArtistRate(models.Model):
    user = models.ForeignKey('lastfm_data.ServiceUser', null=True, blank=True)
    artist = models.ForeignKey(Artist, null=True, blank=True)
    rate = models.PositiveSmallIntegerField(null=True)


class ServiceUser(models.Model):
    username = models.CharField(null=True, blank=True, max_length=256, unique=True)
    objects = ServiceUserQueryset.as_manager()


    def __str__(self):
        return self.username


