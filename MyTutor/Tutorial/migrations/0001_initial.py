# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-25 02:21
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ContractedTutor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='MyUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.CharField(max_length=500)),
                ('myuser', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Tutorial.MyUser')),
            ],
        ),
        migrations.CreateModel(
            name='PrivateTutor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('myuser', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Tutorial.MyUser')),
            ],
        ),
        migrations.CreateModel(
            name='Tutor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timeslot', models.CharField(max_length=336)),
                ('hourly_rate', models.IntegerField()),
                ('myuser', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='Tutorial.MyUser')),
            ],
        ),
        migrations.CreateModel(
            name='TutorialSession',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('starttime', models.CharField(max_length=12)),
                ('status', models.IntegerField()),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Tutorial.Student')),
                ('tutor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Tutorial.Tutor')),
            ],
        ),
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.AddField(
            model_name='privatetutor',
            name='tutor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Tutorial.Tutor'),
        ),
        migrations.AddField(
            model_name='myuser',
            name='wallet',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Tutorial.Wallet'),
        ),
        migrations.AddField(
            model_name='contractedtutor',
            name='tutor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Tutorial.Tutor'),
        ),
    ]
