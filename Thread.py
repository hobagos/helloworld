import threading
import urllib2
from random import shuffle
from gi.repository import Gdk, GdkPixbuf

import Dribbble



class ImageLoader(threading.Thread):
    def __init__(self, image_widgets):
        threading.Thread.__init__(self)

        self.image_widgets = image_widgets
        self._abort = False

    def run(self):
        try:
            dribbble = Dribbble.Dribbble()
            dribbble_shots = dribbble.get_popular()[:len(self.image_widgets)]
            shuffle(dribbble_shots)
        except Exception, e:
            print e
            return

        for i, shot in enumerate(dribbble_shots):
            if self._abort: break
            ImageFromURL(self.image_widgets[i], shot['image_teaser_url'])

    def abort(self):
        self._abort = True

class ImageFromURL(threading.Thread):
    def __init__(self, image_widget, url):
        threading.Thread.__init__(self)

        self.url = url
        self.image_widget = image_widget
        self.start()

    def run(self):
        response = urllib2.urlopen(self.url)

        loader = GdkPixbuf.PixbufLoader()
        loader.write(response.read())
        loader.close()

        Gdk.threads_enter()
        self.image_widget.set_from_pixbuf(loader.get_pixbuf())
        Gdk.threads_leave()
