import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class Handler:

    def onButtonPressed(self, button):
        loading_box = builder.get_object("loading_box")
        loading_box.set_visible(True)
        results_box = builder.get_object("results_box")
        results_box.set_visible(True)


builder = Gtk.Builder()
builder.add_from_file("../ui/main_ui.glade")
builder.connect_signals(Handler())

window = builder.get_object("main_window")
window.show()

Gtk.main()