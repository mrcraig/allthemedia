from django.conf.urls import patterns, url

from allthemedia import views

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name='index'),
    url(r'^about/$', views.about, name='about'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^register/$', views.index, name='register'),
    url(r'^logout/$', views.user_logout, name='logout'),
    url(r'^add_playlist/$', views.add_playlist, name='add_playlist'),
    url(r'^user/(?P<user_name_url>\w+)/(?P<playlist_title_url>\w+)/add_media/$', views.add_media, name='add_media'),
    url(r'^user/(?P<user_name_url>\w+)/(?P<playlist_title_url>\w+)/remove_media/$', views.remove_media, name='remove_media'),
    url(r'^user/(?P<user_name_url>\w+)/$', views.user, name='user'),
    url(r'^user/(?P<user_name_url>\w+)/(?P<playlist_title_url>\w+)/$', 
        views.playlist, name='playlist'),
    )
