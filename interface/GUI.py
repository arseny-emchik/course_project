# coding=utf-8
# =======================================================
#           IMPORTS
# =======================================================
from gi.repository import Gtk


# =======================================================
#                  GUI
# =======================================================
class Handler:

    __builder = None

    __currentKindAlgorithm = 'back_propagation'
    __currentKindDataSet = None

    def __init__(self):
        self.__builder = Gtk.Builder()
        self.__builder.add_from_file("main.glade")
        self.__builder.connect_signals(self)

        window = self.__builder.get_object("quality_assessment")
        window.show_all()

    def onDeleteWindow(self, *args):
        Gtk.main_quit(*args)

    def onExecute(self, *args):
        print 'norm'

    def change_algorithm(self,  widget):
        if widget.get_active():
            self.__currentKindAlgorithm = Gtk.Buildable.get_name(widget)
            self.showText(self.__currentKindAlgorithm) # for test

    def change_kind_data(self, widget):
        if widget.get_active():
            self.__currentKindDataSet = Gtk.Buildable.get_name(widget)
            self.showText(self.__currentKindDataSet) # for test

    def showText(self, line):
        entryForText = self.__builder.get_object('main_text_view')
        #entryForText.get_buffer().set_text('================')
        entryForText.get_buffer().insert(entryForText.get_buffer().get_end_iter(),  "\n" + line)


main = Handler()
Gtk.main()