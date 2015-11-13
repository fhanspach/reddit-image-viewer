# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reddit_api', '0002_auto_20151014_1653'),
    ]

    operations = [
        migrations.AddField(
            model_name='redditimage',
            name='post',
            field=models.URLField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='redditimage',
            name='reddit',
            field=models.ForeignKey(related_name='all_images', to='reddit_api.Reddit', null=True),
        ),
        migrations.AlterField(
            model_name='reddit',
            name='image',
            field=models.ForeignKey(related_name='shown_image', blank=True, to='reddit_api.RedditImage', null=True),
        ),
    ]
