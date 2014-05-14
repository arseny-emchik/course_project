# coding=utf-8
# =======================================================
#           IMPORTS
# =======================================================
from gi.repository import Gtk
from algorithms import back_propagation
from algorithms import control

import _base_GUI

from pybrain.structure import LinearLayer, SigmoidLayer, GaussianLayer, LSTMLayer
from pybrain.structure import MDLSTMLayer, SoftmaxLayer, StateDependentLayer, TanhLayer
FuncArr = ['LinearLayer', 'SigmoidLayer', 'GaussianLayer', 'LSTMLayer', 'MDLSTMLayer', 'SoftmaxLayer', 'StateDependentLayer', 'TanhLayer']

class WinBackPr(_base_GUI.BaseGUI):

    __builder = None
    __root_builder = None
    __window = None

    __file_path = None
    __num_neurons = 1
    __num_cycle = 1
    __percent_train = 1
    __func_name = None

    def __init__(self, root_builder, file_path):
        self.__root_builder = root_builder
        self.__file_path = file_path
        self.__builder = Gtk.Builder()
        self.__builder.add_from_file("bp.glade")
        self.__builder.connect_signals(self)

        self.__setCombobox()

        self.__window = self.__builder.get_object("Back_propagation")
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

    def onExit(self, *args):
        self.__window.destroy()

    def onChangePercent(self, spin):
        self.__percent_train = spin.get_value_as_int()
        #print self.__percent_train

    def onChangeCycle(self, spin):
        self.__num_cycle = spin.get_value_as_int()
        #print self.__num_cycle

    def onChangeNeurons(self, spin):
        self.__num_neurons = spin.get_value_as_int()
        #print self.__num_neurons

    def onExecute(self, *args):
        try:
            back_propagation.load_CSV(self.__file_path)
            network = back_propagation.train(self.__percent_train, self.__num_cycle, self.__num_neurons, self.__func_name)
            data_set = back_propagation.get_data_set(100)
        except:
            text = 'Problem with DataSet.\nSet more percent, please.'
            self._showText(self.__root_builder, text)
            self.__window.destroy()
            return

        if back_propagation.is_binary():
            control.draw_roc(network.activate, data_set)

        control.draw_confusion_matrix(network.activate, data_set)

        text = self._getTextTitle('back_propagation', self.__file_path)
        text += 'Data set is binary: ' + ('true' if back_propagation.is_binary() else 'false') + "\n"
        text += 'Func name: ' + self.__func_name + "\n"
        text += 'Num neurons: %i\n' % self.__num_neurons
        text += 'Num cycle: %i\n' % self.__num_cycle
        text += 'Percent train: %i\n ' % self.__percent_train
        text += back_propagation.getResult(network.activate, data_set)

        self._showText(self.__root_builder, text)
        self.__window.destroy()

Class = WinBackPr