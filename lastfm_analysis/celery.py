# After adding the message broker, add the lines in a new file celery.py that tells
# Celery that we will use the settings in settings.py .


from __future__ import absolute_import

import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mycelery.settings')

from django.conf import settings
from celery import Celery

app = Celery('lastfm_analysis',
             backend='amqp',
             broker='amqp://guest@localhost//')

# This reads, e.g., CELERY_ACCEPT_CONTENT = ['json'] from settings.py:
app.config_from_object('django.conf:settings')

# For autodiscover_tasks to work, you must define your tasks in a file called 'tasks.py'.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

