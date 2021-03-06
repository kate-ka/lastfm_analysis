# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-09-28 08:11
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lastfm_data', '0009_auto_20160822_1046'),
    ]

    operations = [
        migrations.RenameField(
            model_name='playedtrack',
            old_name='user',
            new_name='user_old',
        ),
        migrations.AlterField(
            model_name='playedtrack',
            name='album',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='played_tracks', to='lastfm_data.Album'),
        ),
    ]
