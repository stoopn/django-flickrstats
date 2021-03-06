# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2016-12-27 07:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DayStatistics',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('ts_start', models.IntegerField()),
                ('ts_end', models.IntegerField()),
                ('date_retrieved', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='FlickrUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('userid', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=255)),
                ('date_posted', models.DateTimeField()),
                ('date_taken', models.DateTimeField()),
                ('total_views', models.IntegerField()),
                ('total_comments', models.IntegerField()),
                ('total_favorites', models.IntegerField()),
                ('favorited_by', models.ManyToManyField(through='flickrstats.Favorite', to='flickrstats.FlickrUser')),
            ],
        ),
        migrations.CreateModel(
            name='PhotoStats',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('views', models.IntegerField()),
                ('favorites', models.IntegerField()),
                ('comments', models.IntegerField()),
                ('daystatistics', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flickrstats.DayStatistics')),
                ('photo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flickrstats.Photo')),
            ],
        ),
        migrations.AddField(
            model_name='favorite',
            name='photo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flickrstats.Photo'),
        ),
        migrations.AddField(
            model_name='favorite',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flickrstats.FlickrUser'),
        ),
        migrations.AddField(
            model_name='daystatistics',
            name='photos',
            field=models.ManyToManyField(through='flickrstats.PhotoStats', to='flickrstats.Photo'),
        ),
    ]
