# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-07-12 13:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lastfm_data', '0002_playedtrack_album'),
    ]

    operations = [
        migrations.AddField(
            model_name='playedtrack',
            name='image',
            field=models.URLField(blank=True, null=True),
        ),
    ]
