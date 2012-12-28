import urllib2
import simplejson


class Dribbble:

    def __init__(self):
        self.opener = urllib2.build_opener()

    def get_popular(self):
        req = urllib2.Request("http://api.dribbble.com/shots/popular")
        answer = simplejson.load(
            self.opener.open(req)
            )
        return answer['shots']
