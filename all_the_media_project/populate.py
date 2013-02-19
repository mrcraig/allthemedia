from allthemedia.models import Playlist, Media

p = Playlist(title='Epic Meal Time', views=0)
p.save()
Media(playlist=p, name='EMT - Date With Bacon', url='http://www.youtube.com/watch?v=86eVxuBkqeU').save()
Media(playlist=p, name='EMT - Burly Beaver Sandwich', url='http://www.youtube.com/watch?v=7Ake5iEDtPM').save()
p = Playlist(title='Scott Pilgrim Songs', views=0)
p.save()
Media(playlist=p, name='Garbage Truck', url='http://www.youtube.com/watch?v=fhGu2CDqQqo').save()
Media(playlist=p, name='Black Sheep', url='http://www.youtube.com/watch?v=-jMruFHTwrY').save()
