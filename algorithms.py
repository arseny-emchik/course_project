# coding=utf-8
# =======================================================
#           IMPORTS
# =======================================================
from abc import ABCMeta, abstractmethod, abstractproperty
import csv
import os

#import pybrain
from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.structure import TanhLayer
from pybrain.supervised.trainers import BackpropTrainer
# =======================================================


# =======================================================
#           Neural Network Interface
# =======================================================
class InterfaceNN:
    __metaclass__ = ABCMeta

    @abstractmethod
    def showPlot(self):
        """Show plot"""

    def load_CSV(self, file_name):
        hFile = open(file_name, 'rb')
        self.csv_file = csv.reader(hFile)
        return self.csv_file

    # test method
    def show_CSV(self):
        for row in self.csv_file:
            print row

    def count_inputs(self, number_inputs = -1):
        for row in self.csv_file:
            return len(row) - 1 if number_inputs == -1 else number_inputs
        return 0



# =======================================================
#           Algorithms
# =======================================================
class Class1(InterfaceNN):
    # def data_training(self):
    #     net = buildNetwork(1, 2, 1, bias=True,
    #                        hiddenclass=TanhLayer,
    #                        outclass=TanhLayer,
    #                        recurrent=True)
    #     recCon = FullConnection(net['out'], net['hidden0'])
    #
    # net.addRecurrentConnection(recCon)
    # net.sortModules()
    # # Create a trainer for backprop and train the net.
    # trainer = BackpropTrainer(net, ds, learningrate=0.05)
    # trainer.trainEpochs(1000)

    def showPlot(self):
        return 1


class Class2(InterfaceNN):
    def showPlot(self):
        return 2


# test 1
first = Class1()
second = Class2()
print first.showPlot() + second.showPlot()

#test 2
first.load_CSV('data_sets/iris_dataset.csv')
#first.show_CSV()
print first.count_inputs()



