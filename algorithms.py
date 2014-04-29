# coding=utf-8
# =======================================================
#           IMPORTS
# =======================================================
from abc import ABCMeta, abstractmethod, abstractproperty
import csv

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
        self.hFile = open(file_name, 'rb')
        self.csv_file = csv.reader(self.hFile)
        return self.csv_file

    # test method
    def show_CSV(self):
        for row in self.csv_file:
            print row

    def count_inputs(self, number_inputs = -1):
        self.hFile.seek(0)
        for row in self.csv_file:
            return len(row) - 1 if number_inputs == -1 else number_inputs
        return 0



# =======================================================
#           Algorithms
# =======================================================
class Backprop(InterfaceNN):
    def buildNet(self, hidden_layers, num_outputs, num_inputs, hiddenclass):
        return buildNetwork(num_inputs, hidden_layers, num_outputs)

    def load_data(self, num_inputs, num_outputs):
        ds = SupervisedDataSet(num_inputs, num_outputs)
        self.hFile.seek(0)
        for row in self.csv_file:
            indata = row[:num_inputs]
            outdata = row[num_inputs:]
            ds.addSample(indata, outdata)
        return ds

    def train(self, hidden_layers = 3, num_outputs = 1, num_inputs = -1, hiddenclass = None):
        num_inputs = self.count_inputs() if num_inputs == -1 else num_inputs
        if num_inputs <= 0:
            return

        network = self.buildNet(hidden_layers, num_outputs, num_inputs, hiddenclass)
        data_set = self.load_data(num_inputs, num_outputs)
        trainer = BackpropTrainer(network, data_set)
        print trainer.train()

    def showPlot(self):
        return 1


class Class2(InterfaceNN):
    def showPlot(self):
        return 2


# test 1
first = Backprop()
second = Class2()
print first.showPlot() + second.showPlot()

#test 2
csv_file = first.load_CSV('data_sets/new_iris_dataset.csv')
first.show_CSV()
first.train()
print first.count_inputs()



