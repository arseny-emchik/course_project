# coding=utf-8
# =======================================================
#           IMPORTS
# =======================================================
from gi.repository import Gtk
from algorithms import DBScan

import _base_GUI


class WinDBS(_base_GUI.BaseGUI):

    __builder = None
    __root_builder = None
    __window = None

    __file_path = None
    __eps = 0.1
    __min_samples = 0.1

    def __init__(self, root_builder, file_path):
        self.__root_builder = root_builder
        self.__file_path = file_path
        self.__builder = Gtk.Builder()
        self.__builder.add_from_file("dbs.glade")
        self.__builder.connect_signals(self)

        self.__window = self.__builder.get_object("DBScan")
        self.__window.show_all()

    def onChangeSample(self, spin):
        self.__min_samples = float(spin.get_value())
        #print self.__min_samples

    def onChangeEps(self, spin):
        self.__eps = float(spin.get_value())
        #print self.__eps

    def onExit(self, *args):
        self.__window.destroy()

    def onExecute(self, *args):
        self.__window.destroy() ## ?!!! --

        DBScan.load_CSV(self.__file_path)
        DBScan.train(m_eps=self.__eps, m_min_sales=self.__min_samples)
        DBScan.showPlot2D()
        DBScan.showPlot3D()

Class = WinDBS