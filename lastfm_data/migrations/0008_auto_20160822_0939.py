# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-08-22 09:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lastfm_data', '0007_auto_20160817_1745'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='playedtrack',
            name='image_file',
        ),
        migrations.AlterField(
            model_name='album',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='album_images'),
        ),
    ]
