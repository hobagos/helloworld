import threading
import urllib2
from gi.repository import Gdk, GdkPixbuf

import Dribbble


class ImageLoader(threading.Thread):
    def __init__(self, image_widget):
        threading.Thread.__init__(self)

        self.image_widget = image_widget

    def run(self):
        dribbble = Dribbble.Dribbble()
        dribbble_shots = dribbble.get_popular()

        for shot in dribbble_shots[:1]:
            response = urllib2.urlopen(shot['image_teaser_url'])
            loader = GdkPixbuf.PixbufLoader()
            loader.write(response.read())
            loader.close()
            Gdk.threads_enter()
            self.image_widget.set_from_pixbuf(loader.get_pixbuf())
            Gdk.threads_leave()
