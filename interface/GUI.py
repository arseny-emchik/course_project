# coding=utf-8
# =======================================================
#           IMPORTS
# =======================================================
from gi.repository import Gtk


# =======================================================
#                  GUI
# =======================================================
class Handler:
    def onDeleteWindow(self, *args):
        Gtk.main_quit(*args)

    def onExecute(self, *args):
        print 'yeeeeessss'



builder = Gtk.Builder()
builder.add_from_file("main.glade")
builder.connect_signals(Handler())

window = builder.get_object("quality_assessment")
window.show_all()

Gtk.main()