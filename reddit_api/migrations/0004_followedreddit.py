# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reddit_api', '0003_auto_20151014_1722'),
    ]

    operations = [
        migrations.CreateModel(
            name='FollowedReddit',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('counter', models.BigIntegerField(default=0)),
                ('reddit', models.ForeignKey(to='reddit_api.Reddit')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
