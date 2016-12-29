# app/urls.py

from django.conf.urls import url

from flickrstats import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'charttest', views.charttest, name='charttest'),
]
