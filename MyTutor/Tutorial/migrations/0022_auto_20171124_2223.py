# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-24 14:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tutorial', '0021_auto_20171124_2213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='myuser',
            name='image',
            field=models.ImageField(default=None, upload_to='profile_image'),
        ),
    ]
