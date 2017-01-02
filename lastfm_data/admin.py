from django.contrib import admin
from lastfm_data.models import ServiceUser
from models import PlayedTrack, Artist, Album


class AlbumAdmin(admin.ModelAdmin):
    search_fields = ('name', 'artist__name')
    #list_filter = ('played_tracks__user',)

admin.site.register(PlayedTrack)
admin.site.register(Artist)
admin.site.register(Album, AlbumAdmin)
admin.site.register(ServiceUser)