# coding=utf-8
# =======================================================
#           IMPORTS
# =======================================================
from gi.repository import Gtk
from algorithms import resilient_propagation
from algorithms import control

import _base_GUI

from pybrain.structure import LinearLayer, SigmoidLayer, GaussianLayer, LSTMLayer
from pybrain.structure import MDLSTMLayer, SoftmaxLayer, StateDependentLayer, TanhLayer
FuncArr = ['LinearLayer', 'SigmoidLayer', 'GaussianLayer', 'LSTMLayer', 'MDLSTMLayer', 'SoftmaxLayer', 'StateDependentLayer', 'TanhLayer']

class WinResP(_base_GUI.BaseGUI):

    __builder = None
    __root_builder = None
    __window = None

    __file_path = None
    __num_neurons = 1
    __num_cycle = 1
    __percent_train = 0
    __func_name = None

    def __init__(self, root_builder, file_path):
        self.__root_builder = root_builder
        self.__file_path = file_path
        self.__builder = Gtk.Builder()
        self.__builder.add_from_file("rp.glade")
        self.__builder.connect_signals(self)

        self.__setCombobox()

        self.__window = self.__builder.get_object("resilient_propagation")
        self.__window.show_all()

    def __setCombobox(self):
        liststore = Gtk.ListStore(int, str)
        liststore.append([0, 'Функция активации'])
        for index, data_set in enumerate(FuncArr):
            liststore.append([index, data_set])

        combobox = self.__builder.get_object("func_arr")
        combobox.set_model(liststore)
        cell = Gtk.CellRendererText()
        combobox.pack_start(cell, True)
        combobox.add_attribute(cell, 'text', 1)
        combobox.set_active(0)

    def on_combobox_changed(self, widget, data=None):
        index = widget.get_active()
        model = widget.get_model()
        item = model[index][1]

        if index <= 0:
            return
        self.__func_name = FuncArr[index - 1]

    def onChangePercent(self, spin):
        self.__percent_train = spin.get_value_as_int()

    def onExit(self, *args):
        self.__window.destroy()

    def onChangePercent(self, spin):
        self.__percent_train = spin.get_value_as_int()

    def onChangeCycle(self, spin):
        self.__num_cycle = spin.get_value_as_int()

    def onChangeNeurons(self, spin):
        self.__num_neurons = spin.get_value_as_int()

    def onExecute(self, *args):
        resilient_propagation.load_CSV(self.__file_path)
        network = resilient_propagation.train(self.__percent_train, self.__num_cycle, self.__num_neurons, self.__func_name)
        data_set = resilient_propagation.get_data_set(100)

        text = self._getTextTitle('Resilient propagation', self.__file_path)
        text += 'Data set is binary: ' + ('true' if resilient_propagation.is_binary() else 'false') + "\n"
        text += 'Func name: ' + self.__func_name + "\n"
        self._showText(self.__root_builder, text)
        self.__window.destroy()

        if resilient_propagation.is_binary():
            control.draw_roc(network.activate, data_set)

        control.draw_confusion_matrix(network.activate, data_set)

Class = WinResP