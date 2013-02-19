from django.db import models

class Playlist(models.Model):
    title = models.CharField(max_length=128, unique=True)
    # title of this playlist, primary key
    views = models.IntegerField()
    # number of views on this playlist (only count logged in users ?)
    #collaborators = reference to users who are collaborators
    #creator = (reference to user)
    
    def __unicode__(self):
        return self.title

class Media(models.Model):
    playlist = models.ForeignKey(Playlist)
    # reference to associated playlist
    name = models.CharField(max_length=128, unique = True)
    # name of this media, primary key
    url = models.URLField()
    # url for this media
    source = models.CharField(max_length=128)
    # domain source for this media (ie youtube), could make this 'choices', see API
    thumbnail = models.ImageField(upload_to='/static/thumbnails/')
    # thumbnail for this media (need to fix static url)
    
    def __unicode__(self):
        return self.name
