from django.contrib import admin
from .models import FlickrUser, Photo, DayStatistic, Comment, Favorite, PhotoStat
# Register your models here.


class FlickrUserAdmin(admin.ModelAdmin):
    list_display = ('userid', 'name')


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'date_posted', 'date_taken')


class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'photo', 'date')


class PhotoStatAdmin(admin.ModelAdmin):
    list_display = ('photo', 'daystatistic', 'views', 'favorites', 'comments')


admin.site.register(FlickrUser, FlickrUserAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(DayStatistic)
admin.site.register(Favorite, FavoriteAdmin)
admin.site.register(Comment)
admin.site.register(PhotoStat, PhotoStatAdmin)
