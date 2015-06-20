# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('bookmark', '0002_auto_20150619_0150'),
    ]

    operations = [
        migrations.CreateModel(
            name='Click',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('timestamp', models.DateTimeField(default=django.utils.timezone.now)),
                ('user_id', models.CharField(max_length=16)),
                ('bookmark', models.ForeignKey(to='bookmark.Bookmark')),
            ],
        ),
    ]
