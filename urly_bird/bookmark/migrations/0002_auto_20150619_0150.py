# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bookmark', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookmark',
            name='id',
        ),
        migrations.AlterField(
            model_name='bookmark',
            name='short',
            field=models.CharField(serialize=False, default='', unique=True, primary_key=True, blank=True, max_length=20),
        ),
    ]
