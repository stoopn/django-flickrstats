from __future__ import unicode_literals
from django.db import models
import calendar
import datetime


class FlickrUser(models.Model):
    userid = models.CharField(max_length=100)
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name


class Photo(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=255, default='')
    date_posted = models.DateTimeField()
    date_taken = models.CharField(max_length=20, default='0')
    total_views = models.IntegerField(default=0)
    total_comments = models.IntegerField(default=0)
    total_favorites = models.IntegerField(default=0)
    favorited_by = models.ManyToManyField(
        FlickrUser, through='Favorite', related_name='photos_favorited')
    commented_by = models.ManyToManyField(
        FlickrUser, through='Comment', related_name='photos_commented')

    def __unicode__(self):
        return self.title


class DayStatistic(models.Model):
    date = models.DateField(unique=True)
    ts = models.IntegerField()
    photos = models.ManyToManyField(Photo, through='PhotoStat')
    date_retrieved = models.DateTimeField(auto_now=True)
    completed = models.BooleanField(default=True)

    def __unicode__(self):
        return str(self.date)

    def ts_range(self):
        ts1 = self.ts
        date2 = datetime.date.fromtimestamp(
            self.ts) + datetime.timedelta(days=1)
        ts2 = calendar.timegm(date2.timetuple())
        return [ts1, ts2]


class PhotoStat(models.Model):
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    daystatistic = models.ForeignKey(DayStatistic, on_delete=models.CASCADE)
    views = models.IntegerField()
    favorites = models.IntegerField()
    comments = models.IntegerField()


class Favorite(models.Model):
    user = models.ForeignKey(FlickrUser)
    photo = models.ForeignKey(Photo)
    date = models.DateTimeField()

    def __unicode__(self):
        return self.user.name + " <-> " + self.photo.title + " @ " + str(self.date)


class Comment(models.Model):
    user = models.ForeignKey(FlickrUser)
    photo = models.ForeignKey(Photo)
    date = models.DateTimeField()
