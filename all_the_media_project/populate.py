from allthemedia.models import Playlist, Media, UserProfile
from django.contrib.auth.models import User

print "Populating..."

u1 = User(username="joe", password="bloggs")
u1.save()
up1 = UserProfile(user=u1)
up1.save()
print "created user " + u1.username + ", password " + u1.password

u2 = User(username="bob", password="password1")
u2.save()
up2 = UserProfile(user=u2)
up2.save()
print "created user " + u2.username + ", password " + u2.password

p = Playlist(title='epic meal time', url='epic_meal_time',creator=u1, views=0)
p.save()
print "created " + p.title + " playlist for " + p.creator.username
Media(playlist=p, name='EMT - Date With Bacon', url='http://www.youtube.com/watch?v=86eVxuBkqeU').save()
Media(playlist=p, name='EMT - Burly Beaver Sandwich', url='http://www.youtube.com/watch?v=7Ake5iEDtPM').save()
p = Playlist(title='scott pilgrim songs', creator=u1, url='scott_pilgrim_songs', views=0)
p.save()
print "created " + p.title + " playlist for " + p.creator.username
Media(playlist=p, name='Garbage Truck', url='http://www.youtube.com/watch?v=fhGu2CDqQqo').save()
Media(playlist=p, name='Black Sheep', url='http://www.youtube.com/watch?v=-jMruFHTwrY').save()

print "Done."
