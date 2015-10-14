# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Reddit',
            fields=[
                ('title', models.CharField(max_length=511)),
                ('display_name', models.CharField(max_length=511)),
                ('description', models.TextField()),
                ('over18', models.BooleanField()),
                ('public_description', models.TextField()),
                ('date_created', models.DateTimeField()),
                ('url', models.CharField(max_length=1023, serialize=False, primary_key=True)),
                ('subscribers', models.DecimalField(max_digits=10, decimal_places=0)),
                ('banner_image', models.URLField()),
            ],
        ),
    ]
