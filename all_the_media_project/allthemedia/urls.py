from django.conf.urls import patterns, url

from allthemedia import views

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),
    )
