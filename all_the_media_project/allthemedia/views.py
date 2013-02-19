from django.http import HttpResponse
from django.template import RequestContext, loader
from allthemedia.models import Playlist, Media

def index(request):
    template = loader.get_template('allthemedia/index.html')
    all_playlists = Playlist.objects.all()
    context = RequestContext(request, { 'all_playlists' : all_playlists })
    return HttpResponse(template.render(context))

def about(request):
    template = loader.get_template('allthemedia/about.html')
    context = RequestContext(request, {})
    return HttpResponse(template.render(context))
