from django.test import TestCase
from lastfm_data import lastfm_client
from lastfm_data.models import PlayedTrack
from lastfm_data.tasks import fill_played_tracks


# Create your tests here.


class LastFmClienTestCase(TestCase):
    """
    Tests for our lastfm client's methods
    """

    def test_count_album_tracks(self):
        client = lastfm_client.LastfmClient()
        tracks_count = client.get_album(
            artist_name="Elvis Presley", album_name="The Essential Elvis Presley",)

        self.assertEqual(tracks_count, 52)

    def test_count_album_tracks_for_unknown_album(self):
        client = lastfm_client.LastfmClient()
        tracks_count = client.get_album(
            album_name="qwertyuiop",
            artist_name="Elvis Presley")

        self.assertEqual(tracks_count, 0)




class LastFmCollectTestCase(TestCase):
    """
    Tests for filling db
    """
    def test_fill_played_tracks(self):
        fill_played_tracks('metallist-ka', False)

        tracks = PlayedTrack.objects.all().count()
        pass


