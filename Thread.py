import threading
import urllib2
from gi.repository import Gdk, GdkPixbuf


class ImageLoader(threading.Thread):
    def __init__(self, image_widget, url):
        threading.Thread.__init__(self)
        self.image_widget = image_widget
        self.url = url

    def run(self):
        print "Loading %s" % self.url
        response = urllib2.urlopen(self.url)
        print "Loaded"
        loader = GdkPixbuf.PixbufLoader()
        loader.write(response.read())
        loader.close()
        Gdk.threads_enter()
        self.image_widget.set_from_pixbuf(loader.get_pixbuf())
        Gdk.threads_leave()
