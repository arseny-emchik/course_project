# coding=utf-8
# =======================================================
#           IMPORTS
# =======================================================
from gi.repository import Gtk
from algorithms import kmeans

import _base_GUI

kmeans_init = ["k-means++", "random"]

class WinKMeans(_base_GUI.BaseGUI):

    __builder = None
    __root_builder = None
    __window = None

    __file_path = None
    __kmeans_init = None
    __n_init = 1

    def __init__(self, root_builder, file_path):
        self.__root_builder = root_builder
        self.__file_path = file_path
        self.__builder = Gtk.Builder()
        self.__builder.add_from_file("km.glade")
        self.__builder.connect_signals(self)

        self.__setCombobox1()

        self.__window = self.__builder.get_object("kmeans")
        self.__window.show_all()

    def __setCombobox1(self):
        liststore = Gtk.ListStore(int, str)
        liststore.append([0, 'Не выбрано'])
        for index, data_set in enumerate(kmeans_init):
            liststore.append([index, data_set])

        combobox = self.__builder.get_object("kmeans_init")
        combobox.set_model(liststore)
        cell = Gtk.CellRendererText()
        combobox.pack_start(cell, True)
        combobox.add_attribute(cell, 'text', 1)
        combobox.set_active(0)

    def on_kmeans_init_changed(self, widget, data=None):
        index = widget.get_active()
        model = widget.get_model()
        item = model[index][1]

        if index <= 0:
            return
        self.__kmeans_init = kmeans_init[index - 1]

    def onChangeNInit(self, spin):
        self.__n_init = spin.get_value_as_int()

    def onExit(self, *args):
        self.__window.destroy()

    def onExecute(self, *args):
        kmeans.load_CSV(self.__file_path)
        km = kmeans.train(init=self.__kmeans_init, n_init=self.__n_init)
        kmeans.showPlot(km)

        text = self._getTextTitle('K-means', self.__file_path)
        text += kmeans.getResult(km)
        self._showText(self.__root_builder, text)

        self.__window.destroy()

Class = WinKMeans