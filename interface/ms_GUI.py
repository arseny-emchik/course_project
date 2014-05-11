# coding=utf-8
# =======================================================
#           IMPORTS
# =======================================================
from gi.repository import Gtk
from algorithms import mshift

import _base_GUI


class WinMSift(_base_GUI.BaseGUI):

    __builder = None
    __root_builder = None
    __window = None

    __file_path = None
    __quantile = 0.15
    __cluster_all = False

    def __init__(self, root_builder, file_path):
        self.__root_builder = root_builder
        self.__file_path = file_path
        self.__builder = Gtk.Builder()
        self.__builder.add_from_file("ms.glade")
        self.__builder.connect_signals(self)

        self.__window = self.__builder.get_object("mshift")
        self.__window.show_all()

    def onChangeQuantile(self, spin):
        self.__quantile = float(spin.get_value())
        print self.__quantile

    def onCheck1(self, widget):
        if widget.get_active():
            self.__cluster_all = True
        else:
            self.__cluster_all = False

        print self.__cluster_all

    def onExit(self, *args):
        self.__window.destroy()

    def onExecute(self, *args):
        self.__window.destroy() ## ?!!! --

        mshift.load_CSV(self.__file_path)
        mean_shift = mshift.train(m_quantile=self.__quantile, m_cluster_all=self.__cluster_all)
        data_set = mshift.get_data_set(100)
        mshift.showPlot3D()

Class = WinMSift