# coding=utf-8
# =======================================================
#           IMPORTS
# =======================================================
from gi.repository import Gtk
from algorithms import support_vector
from algorithms import control

import _base_GUI

kernels = ["rbf", "linear", "poly", "sigmoid", "precomputed"]

class WinSepVector(_base_GUI.BaseGUI):

    __builder = None
    __root_builder = None
    __window = None

    __file_path = None
    __kernel = None
    __percents = 1

    def __init__(self, root_builder, file_path):
        self.__root_builder = root_builder
        self.__file_path = file_path
        self.__builder = Gtk.Builder()
        self.__builder.add_from_file("sp.glade")
        self.__builder.connect_signals(self)

        self.__setCombobox1()

        self.__window = self.__builder.get_object("support_vector")
        self.__window.show_all()

    def __setCombobox1(self):
        liststore = Gtk.ListStore(int, str)
        liststore.append([0, 'Не выбрано'])
        for index, data_set in enumerate(kernels):
            liststore.append([index, data_set])

        combobox = self.__builder.get_object("kernels")
        combobox.set_model(liststore)
        cell = Gtk.CellRendererText()
        combobox.pack_start(cell, True)
        combobox.add_attribute(cell, 'text', 1)
        combobox.set_active(0)

    def on_kernels_changed(self, widget, data=None):
        index = widget.get_active()
        model = widget.get_model()
        item = model[index][1]

        if index <= 0:
            return
        self.__kernel = kernels[index - 1]
        #print self.__kernel

    def onChangePercents(self, spin):
        self.__percents = spin.get_value_as_int()
        #print self.__percents

    def onExit(self, *args):
        self.__window.destroy()

    def onExecute(self, *args):
        try:
            support_vector.load_CSV(self.__file_path)
            clf = support_vector.train(self.__percents, kernel=self.__kernel)
            data_set = support_vector.get_data_set(100)

            if support_vector.is_binary():
                control.draw_roc(clf.predict, data_set)
            control.draw_confusion_matrix(clf.predict, data_set)

            text = self._getTextTitle('Support vector machines', self.__file_path)
            text += 'Data set is binary: ' + ('true' if support_vector.is_binary() else 'false')
            self._showText(self.__root_builder, text)
            self.__window.destroy()
        except:
            text = 'Problem with DataSet.\nSet more percent, please.'
            self._showText(self.__root_builder, text)
            self.__window.destroy()
            return

Class = WinSepVector