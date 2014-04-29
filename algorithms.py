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
        self.row_count = sum(1 for row in self.csv_file)
        return self.csv_file

    # test method
    def show_CSV(self):
        self.hFile.seek(0)
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

    def load_data(self, percent, num_inputs, num_outputs):
        ds = SupervisedDataSet(num_inputs, num_outputs)
        self.hFile.seek(0)
        for i in range(int(self.row_count*(float(percent)/100.0))):
            data = self.csv_file.next()
            indata = data[:num_inputs]
            outdata = data[num_inputs:]
            ds.addSample(indata, outdata)
        return ds

    def train(self,
              percent,
              hidden_layers = 3,
              num_outputs = 1,
              num_inputs = -1,
              hiddenclass = None):
        num_inputs = self.count_inputs() if num_inputs == -1 else num_inputs
        if num_inputs <= 0:
            return

        network = self.buildNet(hidden_layers, num_outputs, num_inputs, hiddenclass)
        data_set = self.load_data(percent, num_inputs, num_outputs)
        trainer = BackpropTrainer(network, data_set)
        for i in range(30):
            trainer.train()
        #trainer.trainUntilConvergence()
        return network


    def showPlot(self):
        return 1


class Class2(InterfaceNN):
    def showPlot(self):
        return 2



#test
b = Backprop()
csv_file = b.load_CSV('data_sets/new_iris_dataset.csv')
b.show_CSV()
print b.count_inputs()
network = b.train(90)
print network.activate([5.1, 3.5, 1.4, 0.2])




