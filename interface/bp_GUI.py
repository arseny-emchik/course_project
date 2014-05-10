# coding=utf-8
# =======================================================
#           IMPORTS
# =======================================================
from gi.repository import Gtk
from algorithms import back_propagation
from algorithms import control

from pybrain.structure import LinearLayer, SigmoidLayer, GaussianLayer, LSTMLayer
from pybrain.structure import MDLSTMLayer, SoftmaxLayer, StateDependentLayer, TanhLayer
FuncArr = ['LinearLayer', 'SigmoidLayer', 'GaussianLayer', 'LSTMLayer', 'MDLSTMLayer', 'SoftmaxLayer', 'StateDependentLayer', 'TanhLayer']

# class WinBackPr:
#
#     __builder = None
#     __root_builder = None
#     __window = None
#
#     __currentKindDataSet = None
#     __file_path = None
#
#     __percent_train = 0
#
#     def __init__(self, root_builder, file_path):
#         self.__root_builder = root_builder
#         self.__file_path = file_path
#         self.__builder = Gtk.Builder()
#         self.__builder.add_from_file("win1.glade")
#         self.__builder.connect_signals(self)
#
#         self.__window = self.__builder.get_object("dialog1")
#         self.__window.show_all()
#
#         text = 'New win has created!\n'
#         text += 'Params:\n'
#         text += 'Algorithms: Back propagation\n'
#         text += 'Data set path: ' + file_path
#
#         self.showText(self.__root_builder, text)
#         self.showText(self.__builder, 'file path is ' + file_path)
#
#     def __clearTextView(self, builder):
#         entryForText = builder.get_object('main_text_view')
#         entryForText.get_buffer().set_text('')
#
#     def showText(self, builder, line):
#         self.__clearTextView(builder)
#         entryForText = builder.get_object('main_text_view')
#
#         line += '\n=====================================\n'
#         entryForText.get_buffer().insert(entryForText.get_buffer().get_end_iter(), line)
#
#     def onChangePercent(self, spin):
#         self.__percent_train = spin.get_value_as_int()
#
#     def onSomeValue(self, entry):
#         a = entry.get_chars(0, -1)
#         print a
#
#     def onCheck1(self, widget):
#         if widget.get_active():
#             print 'true'
#         else:
#             print 'false'
#
#     def onExit(self, *args):
#         self.__window.destroy()


class WinBackPr:

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

    def __clearTextView(self, builder):
        entryForText = builder.get_object('main_text_view')
        entryForText.get_buffer().set_text('')

    def showText(self, builder, line):
        self.__clearTextView(builder)
        entryForText = builder.get_object('main_text_view')

        line += '\n=====================================\n'
        entryForText.get_buffer().insert(entryForText.get_buffer().get_end_iter(), line)

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
        self.__window.destroy() ## ?!!! --

        back_propagation.load_CSV(self.__file_path)
        network = back_propagation.train(self.__percent_train, self.__num_cycle, self.__num_neurons, self.__func_name)
        data_set = back_propagation.get_data_set(100)

        text = 'New win has created!\n'
        text += 'Params:\n'
        text += 'Algorithms: Back propagation\n'
        text += 'Data set path: ' + self.__file_path + "\n"
        text += 'Data set is binary: ' + ('true' if back_propagation.is_binary() else 'false') + "\n"
        text += 'Func name: ' + self.__func_name

        # text += 'Num neurons: ' + self.__num_neurons + "\n"
        # text += 'Num cycle: ' + self.__num_cycle + "\n"
        # text += 'Percent train: ' + self.__percent_train
        #text +=

        self.showText(self.__root_builder, text)


        if back_propagation.is_binary():
            control.draw_roc(network.activate, data_set)

        control.draw_confusion_matrix(network.activate, data_set)

Class = WinBackPr