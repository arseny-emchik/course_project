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

from sklearn.metrics import confusion_matrix
import pylab as pl
# =======================================================

# =======================================================
#           Neural Network Interface
# =======================================================
class InterfaceNN:
    __metaclass__ = ABCMeta

    @abstractmethod
    def showPlot(self):
        """Show plot"""

    @abstractmethod
    def train(self,
              cycles,
              percent,
              hidden_layers=3,
              num_outputs=1,
              num_inputs=-1,
              hiddenclass=None):
        """train net"""

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

    def count_inputs(self, number_inputs=-1):
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

    def get_data_set(self, percent, num_inputs=-1, num_outputs=1):
        num_inputs = self.count_inputs() if num_inputs == -1 else num_inputs
        if num_inputs <= 0 or num_outputs <= 0 or percent <= 0:
            return

        ds = SupervisedDataSet(num_inputs, num_outputs)
        self.hFile.seek(0)
        for i in range(int(self.row_count * (float(percent) / 100.0))):
            data = self.csv_file.next()
            indata = data[:num_inputs]
            outdata = data[num_inputs:]
            ds.addSample(indata, outdata)
        return ds

    def train(self,
              cycles,
              percent,
              hidden_layers=3,
              num_outputs=1,
              num_inputs=-1,
              hiddenclass=None):
        num_inputs = self.count_inputs() if num_inputs == -1 else num_inputs
        if num_inputs <= 0 or num_outputs <= 0 or cycles <= 0 or (percent > 100 or percent <= 0):
            return

        network = self.buildNet(hidden_layers, num_outputs, num_inputs, hiddenclass)
        data_set = self.get_data_set(percent, num_inputs, num_outputs)
        trainer = BackpropTrainer(network, data_set)

        for i in range(cycles):
            trainer.train()

        return network

    def showPlot(self):
        return 1

# =======================================================
#           CONTROL
# =======================================================
class Control:
    def calculate_entire_ds(self, network, data_set):
        y_true = []
        y_predict = []

        for i in data_set:
            predict = int(round(network.activate(i[0])))
            true = int(i[1][0])
            y_predict.append(predict)
            y_true.append(true)

        # print "{} {}".format(predict,true)
        # print y_true
        # print y_predict
        return y_true, y_predict

    def draw_confusion_matrix(self, network, data_set):
        y_true, y_predict = self.calculate_entire_ds(network, data_set)
        cm = confusion_matrix(y_true, y_predict)
        pl.matshow(cm)
        pl.title('Confusion matrix')
        pl.colorbar()
        pl.ylabel('True label')
        pl.xlabel('Predicted label')
        pl.show()



#test
c = Control()
b = Backprop()

b.load_CSV('data_sets/new_iris_dataset.csv')
network = b.train(60, 90)
data_set = b.get_data_set(100)

c.draw_confusion_matrix(network, data_set)
#print "Predict y:\n{}".format(c.y_predict)
