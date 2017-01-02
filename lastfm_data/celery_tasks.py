from celery import group
from lastfm_data.tasks import fill_played_tracks


@app.task
def task_get_played_tracks(username, page):
    fill_played_tracks()
