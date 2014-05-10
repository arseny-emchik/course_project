# coding=utf-8
# =======================================================
#           IMPORTS
# =======================================================
from gi.repository import Gtk

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

    __currentKindDataSet = None
    __file_path = None

    __percent_train = 0

    def __init__(self, root_builder, file_path):
        self.__root_builder = root_builder
        self.__file_path = file_path
        self.__builder = Gtk.Builder()
        self.__builder.add_from_file("win1.glade")
        self.__builder.connect_signals(self)

        self.__window = self.__builder.get_object("dialog1")
        self.__window.show_all()

        text = 'New win has created!\n'
        text += 'Params:\n'
        text += 'Algorithms: Back propagation\n'
        text += 'Data set path: ' + file_path

        self.showText(self.__root_builder, text)
        self.showText(self.__builder, 'file path is ' + file_path)

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

    def onSomeValue(self, entry):
        a = entry.get_chars(0, -1)
        print a

    def onCheck1(self, widget):
        if widget.get_active():
            print 'true'
        else:
            print 'false'

    def onExit(self, *args):
        self.__window.destroy()

Class = WinBackPr