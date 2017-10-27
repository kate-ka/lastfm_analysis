from celery import group, task

from lastfm_data import lastfm_client
from lastfm_data.models import ServiceUser
from lastfm_data.tasks import fill_played_tracks


@task
def task_handle_tracks_page(username, page_number):
    fill_played_tracks(username, page_from=page_number, page_to=page_number)


def fill_user_tracks(username):
    """
    Get all tracks from lastfm for given username and store in db.
    """
    ServiceUser.objects.get_or_create(username=username)

    client = lastfm_client.LastfmClient()

    # Get total number of listened tracks and calculate count of pages
    info = client.get_info(username)

    if not info:
        #TODO error handling
        pass

    played_tracks_count = int(info['playcount'])
    pages_count = played_tracks_count // 1000

    # Create tasks to handle each page separately
    g = group(
        task_handle_tracks_page.subtask(args=(username, page_number))
        for page_number
        in range(1, pages_count + 1)
    )

    # Put tasks into queue and wait until all pages will be handled
    g().get()

    return True



