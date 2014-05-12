# coding=utf-8
# =======================================================
#           IMPORTS
# =======================================================
from gi.repository import Gtk
from algorithms import decision_tree
from algorithms import control

import _base_GUI

tree_criterion = ["gini", "entropy"]
max_features = ["auto", "sqrt", "log2"]

class WinDecTree(_base_GUI.BaseGUI):

    __builder = None
    __root_builder = None
    __window = None

    __file_path = None
    __percent_train = 1
    __tree_criterion = None
    __max_features = None

    def __init__(self, root_builder, file_path):
        self.__root_builder = root_builder
        self.__file_path = file_path
        self.__builder = Gtk.Builder()
        self.__builder.add_from_file("dt.glade")
        self.__builder.connect_signals(self)

        self.__setCombobox1()
        self.__setCombobox2()

        self.__window = self.__builder.get_object("decision_tree")
        self.__window.show_all()

    def __setCombobox1(self):
        liststore = Gtk.ListStore(int, str)
        liststore.append([0, 'Не выбрано'])
        for index, data_set in enumerate(tree_criterion):
            liststore.append([index, data_set])

        combobox = self.__builder.get_object("tree_criterion")
        combobox.set_model(liststore)
        cell = Gtk.CellRendererText()
        combobox.pack_start(cell, True)
        combobox.add_attribute(cell, 'text', 1)
        combobox.set_active(0)

    def __setCombobox2(self):
        liststore = Gtk.ListStore(int, str)
        liststore.append([0, 'Не выбрано'])
        for index, data_set in enumerate(max_features):
            liststore.append([index, data_set])

        combobox = self.__builder.get_object("max_features")
        combobox.set_model(liststore)
        cell = Gtk.CellRendererText()
        combobox.pack_start(cell, True)
        combobox.add_attribute(cell, 'text', 1)
        combobox.set_active(0)

    def on_combobox1_changed(self, widget, data=None):
        index = widget.get_active()
        model = widget.get_model()
        item = model[index][1]

        if index <= 0:
            return
        self.__tree_criterion = tree_criterion[index - 1]

    def on_combobox2_changed(self, widget, data=None):
        index = widget.get_active()
        model = widget.get_model()
        item = model[index][1]

        if index <= 0:
            return
        self.__max_features = max_features[index - 1]

    def onChangePercent(self, spin):
        self.__percent_train = spin.get_value_as_int()

    def onExit(self, *args):
        self.__window.destroy()

    def onExecute(self, *args):
        self.__window.destroy() ## ?!!! --

        decision_tree.load_CSV(self.__file_path)
        clf = decision_tree.train(self.__percent_train, criterion=self.__tree_criterion, max_features=self.__max_features)
        data_set = decision_tree.get_data_set(100)

        text = self._getTextTitle('Decision Tree', self.__file_path)
        text += 'Data set is binary: ' + ('true' if decision_tree.is_binary() else 'false') + "\n"
        text += 'Tree criterion: ' + self.__tree_criterion + "\n"
        text += 'Max features: ' + self.__max_features

        self._showText(self.__root_builder, text)

        if decision_tree.is_binary():
            control.draw_roc(clf.predict, data_set)

        control.draw_confusion_matrix(clf.predict, data_set)

Class = WinDecTree