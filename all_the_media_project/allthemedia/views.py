from urlparse import urlparse
from string import lower
from django.http import HttpResponse
from django.template import RequestContext, loader
from allthemedia.models import Playlist, Media
from django.contrib.auth.models import User
from allthemedia.models import UserProfile
from allthemedia.models import UserForm, UserProfileForm
from allthemedia.models import PlaylistForm, MediaForm
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def index(request):
    template = loader.get_template('allthemedia/index.html')
    all_playlists = Playlist.objects.all()
    context_dict = { 'all_playlists' : all_playlists }
    user_list = UserProfile.objects.all()
    for u in user_list:
        u.url = u.user.username
    context_dict['user_list'] = user_list
    context = RequestContext(request, context_dict)
    return HttpResponse(template.render(context))

def about(request):
    template = loader.get_template('allthemedia/about.html')
    context = RequestContext(request, {})
    return HttpResponse(template.render(context))

def user(request, user_name_url):
    template = loader.get_template('allthemedia/userprofile.html')

    context_dict = {'user_name_url': user_name_url }
    user = User.objects.filter(username=user_name_url)
    if user:
        playlists = Playlist.objects.filter(creator=user)
        context_dict['playlists'] = playlists
        playlist_urls = {}
        for pl in playlists:
            playlist_urls[pl.title] = encode_playlist(pl.title)
            context_dict['playlist_urls'] = playlist_urls
        print playlist_urls
        
    context = RequestContext(request, context_dict)
    return HttpResponse(template.render(context))

def register(request):
    context = RequestContext(request)
    registered = False
    if request.method == 'POST':
        uform = UserForm(data = request.POST)
        pform = UserProfileForm(data = request.POST)
        if uform.is_valid() and pform.is_valid():
            user = uform.save()
            # form brings back a plain text string, not an encrypted password
            pw = user.password
            # thus we need to use set password to encrypt the password string
            user.set_password(pw)
            user.save()
            profile = pform.save(commit = False)
            profile.user = user
            profile.save()
            registered = True
        else:
            print uform.errors, pform.errors
    else:
        uform = UserForm()
        pform = UserProfileForm()
        
    return render_to_response('allthemedia/register.html', 
                              {'uform': uform, 'pform': 
                               pform, 'registered': registered },
                              context)

def playlist(request, user_name_url, playlist_title_url):
    context = RequestContext(request)
    user = User.objects.filter(username=user_name_url)
    if user:
        context_dict = {'user': user}
        playlist_title = decode_playlist(playlist_title_url)
        pl = Playlist.objects.filter(title = playlist_title)
        if pl:
            context_dict['playlist'] = pl
            media = Media.objects.filter(playlist=pl)
            context_dict['media'] = media
            context_dict['playlist_title'] = playlist_title
            context_dict['playlist_url'] = playlist_title_url
            return render_to_response('allthemedia/playlist.html',
                                      context_dict,
                                      context)
        else:
            print "This user has no such playlist " + playlist_title
            return HttpResponseRedirect("/allthemedia/")
    else:
        print "No such user, " + user_name_url
        return HttpResponseRedirect("/allthemedia/")
    

def user_login(request):
    context = RequestContext(request)
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                  # Redirect to index page.
                return HttpResponseRedirect("/allthemedia/")
            else:
                # Return a 'disabled account' error message
                return HttpResponse("Your account is disabled.")
        else:
            # Return an 'invalid login' error message.
            print  "invalid login details " + username + " " + password
            return render_to_response('allthemedia/login.html', {}, context)
    else:
        # the login is a  GET request, so just show the user the login form.
        return render_to_response('allthemedia/login.html', {}, context)

@login_required
def user_logout(request):
    context = RequestContext(request)
    logout(request)
    return HttpResponseRedirect('/allthemedia/')

@login_required    
def add_playlist(request):
    context = RequestContext(request)
    if request.method == 'POST':
        form = PlaylistForm(request.POST)
        if form.is_valid():
            pl = form.save(commit = False)
            pl.title = lower(pl.title)
            pl.views = 0
            pl.creator = request.user
            pl.save()
            return index(request)
        else:
            # form not valid, show form again
            pass
    else:
        # GET request, so show form
        form = PlaylistForm()
    return render_to_response('allthemedia/add_playlist.html',
                              {'form':form}, context)

def add_media(request, playlist_title_url):
    context = RequestContext(request)
    playlist_title = decode_playlist(playlist_title_url)
    pl = Playlist.objects.get(title = playlist_title)
    user_name_url = pl.creator.username
    if request.method == 'POST':
        form = MediaForm(request.POST)
        if form.is_valid():
            m = form.save(commit = False)
            m.playlist = pl
            src = get_source(m.url)
            m.source = src
            m.save()
            return playlist(request, playlist_title_url, user_name_url)
        else:
            print form.errors
    else:
        form = MediaForm()
    return render_to_response('allthemedia/add_media.html',
                              {'playlist_title_url': playlist_title_url,
                               'playlist_title': playlist_title,
                               'user_name_url': user_name_url,
                               'form' : form},
                              context)
            
            
def encode_playlist(playlist_title):
    return lower(playlist_title.replace(' ', '_'))

def decode_playlist(playlist_url):
    return playlist_url.replace('_', ' ')

def get_source(media_url):
    s = urlparse(media_url)
    return s.hostname
