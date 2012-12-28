from UserDict import UserDict
import os
import glib
import json

DEBUG = True
NAME = "helloworld"


class Settings(UserDict):

    if DEBUG:
        FILENAME = os.path.join(
            os.path.dirname(__file__),
            "settings.json"
            )
    else:
        FILENAME = os.path.join(
            glib.get_user_config_dir(),
            NAME,
            'settings.json'
            )

    DEFAULT_PREFERENCES = {
        'width': 500,
        'height': 500,
        'maximized': False,
    }

    def save(self):
        if not os.path.exists(os.path.dirname(self.FILENAME)):
            os.makedirs(os.path.dirname(self.FILENAME))

        f = open(self.FILENAME, 'w')
        f.write(json.dumps(self.data, indent=4))
        f.flush()
        f.close()

    def load(self):
        if not os.path.exists(self.FILENAME):
            self.data = self.DEFAULT_PREFERENCES
            self.save()
            return

        try:
            f = open(self.FILENAME, 'r')
            self.data = json.loads(f.read())
            f.close()
        except:
            print "ERROR: Could not read preferences " +\
                  "file. Loading default values."
            self.data = self.DEFAULT_PREFERENCES
            self.save()
            return
