import gi
gi.require_version('Gtk', '3.0')
from gi.repository import GLib, Gtk, GObject
from ui.ui import Handler

def app_main():
    builder = Gtk.Builder()
    builder.add_from_file("ui/main_ui.glade")
    builder.connect_signals(Handler(builder))

    main_window = builder.get_object("main_window")
    main_window.set_title("IQPlayground")
    main_window.show()
    main_window.connect("delete-event", Gtk.main_quit)

if __name__ == "__main__":
    app_main()
    Gtk.main()