# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-24 11:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tutorial', '0018_merge_20171124_1942'),
    ]

    operations = [
        migrations.AddField(
            model_name='tutor',
            name='average',
            field=models.DecimalField(decimal_places=1, default=0, max_digits=2),
        ),
        migrations.AddField(
            model_name='tutor',
            name='reviewd_times',
            field=models.IntegerField(default=0),
        ),
    ]
