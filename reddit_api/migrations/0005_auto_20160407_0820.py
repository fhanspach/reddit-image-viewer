# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reddit_api', '0004_followedreddit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reddit',
            name='banner_image',
            field=models.URLField(null=True, blank=True),
        ),
    ]
