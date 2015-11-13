# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reddit_api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RedditImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.URLField()),
                ('reputation', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='reddit',
            name='image',
            field=models.ForeignKey(blank=True, to='reddit_api.RedditImage', null=True),
        ),
    ]
