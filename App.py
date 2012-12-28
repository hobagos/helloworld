#!/usr/bin/python

from gi.repository import Gtk, Gdk, Gio, Granite, Notify

import Settings


class MyWindow(Gtk.Window):

    MIN_WIDTH = 400
    MIN_HEIGHT = 300

    def __init__(self):
        Gtk.Window.__init__(self,
            Gtk.WindowType.TOPLEVEL,
            title="Hello World")

        self.settings = Settings.Settings()
        self.settings.load()

        self.set_size_request(self.MIN_WIDTH, self.MIN_HEIGHT)

        self.connect("window-state-event", self.state_handler)
        self.connect("delete-event", self.destroy_handler)

        self.load_state()
        self.load_ui()

    def load_ui(self):
        vbox = Gtk.VBox()

        toolbar = Gtk.Toolbar.new()
        vbox.pack_start(toolbar, False, True, 0)

        menu = Gtk.Menu.new()
        notify_item = Gtk.MenuItem.new_with_label("Notify")
        notify_item.connect("activate", self.menu_notify)
        menu.append(notify_item)
        about_item = Gtk.MenuItem.new_with_label("About Dialog")
        menu.append(about_item)
        menu_item = Gtk.MenuItem.new_with_label("Quit")
        menu_item.connect('activate', self.destroy_handler)
        menu.append(menu_item)

        separator = Gtk.SeparatorToolItem.new()
        separator.set_expand(True)
        separator.set_draw(False)
        toolbar.insert(separator, -1)
        appmenu = Granite.WidgetsAppMenu.new(menu)
        toolbar.insert(appmenu, -1)

        welcome = Granite.WidgetsWelcome.new(
            "Hello World",
            "Sample program")
        welcome.drag_dest_set(
            Gtk.DestDefaults.ALL,
            [], Gdk.DragAction.COPY)
        welcome.connect(
            "drag-data-received",
            self.on_drag_data_received)
        welcome.drag_dest_add_uri_targets()
        vbox.pack_start(welcome, True, True, 0)

        self.add(vbox)

    def on_drag_data_received(self,
            widget, context, x, y,
            data, info, time):
        print data.get_data()

    def load_state(self):
        self.set_default_size(
            self.settings['width'],
            self.settings['height'])
        if self.settings['maximized']:
            self.maximize()
        #self.set_position(Gtk.WindowPosition.CENTER)

    def save_state(self):
        if not self.settings['maximized']:
            width, height = self.get_size()
            self.settings['width'] = width
            self.settings['height'] = height
        self.settings.save()

    def state_handler(self, widget, event):
        if widget.get_window().get_state() &\
                    Gdk.WindowState.MAXIMIZED:
            self.settings["maximized"] = True
        else:
            self.settings["maximized"] = False

    def destroy_handler(self, *args):
        self.save_state()
        self.get_application().quit()

    def menu_notify(self, event):
        Notify.init(Settings.NAME)
        notification = Notify.Notification.new(
            'Hello!',
            'Menu notification',
            'dialog-information'
        )
        notification.show()


class App(Gtk.Application):
    def __init__(self):
        Gtk.Application.__init__(
            self,
            application_id="apps.test.helloworld",
            flags=Gio.ApplicationFlags.FLAGS_NONE)
        self.connect("activate", self.activate)

    def activate(self, data=None):
        window = MyWindow()
        window.set_application(self)
        window.show_all()
        self.add_window(window)


if __name__ == "__main__":
    app = App()
    argv = "test.py"
    app.run(None)
