# coding=utf-8
# =======================================================
#           IMPORTS
# =======================================================
from gi.repository import Gtk

import sys
import os
from os import listdir
from os.path import isfile, join

# import files
import bp_GUI as Bp
import rp_GUI as Rp
import dt_GUI as Dt

from algorithms import DBScan
from algorithms import mshift
from algorithms import support_vector
from algorithms import control

DATA_SETS_PATH = os.getcwd() + '/../data_sets/'
DataSetArr = [f for f in listdir(DATA_SETS_PATH) if isfile(join(DATA_SETS_PATH, f))]

# =======================================================
#                  GUI
# =======================================================
class Handler:

    __builder = None

    __currentKindAlgorithm = 'back_propagation'
    __currentKindDataSet = 'data_set_default'

    __file_path = 'No file' # for file chooser
    __file_name = 'No file' # for default files

    def __init__(self):
        self.__builder = Gtk.Builder()
        self.__builder.add_from_file("main.glade")
        self.__builder.connect_signals(self)

        self.__setCombobox()

        window = self.__builder.get_object("quality_assessment")
        window.show_all()

    def __setCombobox(self):
        liststore = Gtk.ListStore(int, str)
        liststore.append([0, 'Выберите Data Set'])
        for index, data_set in enumerate(DataSetArr):
            liststore.append([index, data_set])

        combobox = self.__builder.get_object("combobox1")
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
        self.__file_name = DataSetArr[index - 1]

        self.showText("ComboBox Active Text is " + self.__file_name) # for test

    def onFileSet(self, widget):
        self.__file_path = widget.get_file().get_path()
        self.showText("File path is " + self.__file_path) # for test

    def onDeleteWindow(self, *args):
        Gtk.main_quit(*args)
        sys.exit(0)

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
        entryForText.get_buffer().insert(entryForText.get_buffer().get_end_iter(), line + '\n=============\n')

    def onExecute(self, *args):
        self.showText('!') # for test
        self.showText(self.__currentKindDataSet) # for test

        if self.__currentKindDataSet == 'data_set_default':
            file_path = DATA_SETS_PATH + self.__file_name
        elif self.__currentKindDataSet == 'data_set_file':
            file_path = self.__file_path
        else:
            self.showText('Error data set')
            return

        self.__createNewWindow(file_path)

    def __createNewWindow(self, file_path):
        if self.__currentKindAlgorithm == 'back_propagation':
            main = Bp.Class(self.__builder, file_path)
        elif self.__currentKindAlgorithm == 'resilient_propagation':
            main = Rp.Class(self.__builder, file_path)
        elif self.__currentKindAlgorithm == 'decision_trees':
            main = Dt.Class(self.__builder, file_path)
        elif self.__currentKindAlgorithm == 'k_means':
            main = Bp.Class(self.__builder, file_path)
        elif self.__currentKindAlgorithm == 'support_vector':
            main = Bp.Class(self.__builder, file_path)
        elif self.__currentKindAlgorithm == 'mean_shift':
            main = Bp.Class(self.__builder, file_path)
        else:
            self.showText('Error create new win')
            return

        Gtk.main()


main = Handler()
Gtk.main()