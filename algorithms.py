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

from sklearn.metrics import confusion_matrix, roc_curve, auc
import pylab as pl
from random import randint
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

        self.binary = False
        if self.get_levels() == 2:
            self.binary = True

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

    def get_levels(self):
        data_set = self.get_data_set(100)
        levels = []
        for i in data_set['target']:
            level = int(i)
            if level not in levels:
                levels.append(level)
        return levels

    def get_data_set_array_with_specific_level(self, level):
        data_set = self.get_data_set(100)
        result = []
        for i in data_set:
            current_level = int(i[1])
            if current_level == level:
                result.append(i)
        return result

    def is_binary(self):
        return self.binary

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

    def get_data_set_by_levels(self, percent, num_inputs=-1, num_outputs=1):
        levels = self.get_levels()
        num_inputs = self.count_inputs() if num_inputs == -1 else num_inputs
        if num_inputs <= 0 or num_outputs <= 0 or percent <= 0:
            return

        ds = SupervisedDataSet(num_inputs, num_outputs)
        num_rows = int(self.row_count * (float(percent) / 100.0))
        num_rows_in_class = int(num_rows/len(levels))

        for level in levels:
            data_set = self.get_data_set_array_with_specific_level(level)
            used_samples = []
            for i in range(num_rows_in_class):
                added = False
                while(not added):
                    row = randint(0, num_rows_in_class)
                    if row not in used_samples:
                        used_samples.append(row)
                        sample = data_set[row]
                        ds.addSample(sample[0], sample[1])
                        added = True
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

    def draw_roc(self, network, data_set):
        y_true, y_predict = self.calculate_entire_ds(network, data_set)
        fpr, tpr, thresholds = roc_curve(y_true, y_predict)
        roc_auc = auc(fpr, tpr)
        print("Area under the ROC curve : %f" % roc_auc)

        # Plot ROC curve
        pl.clf()
        pl.plot(fpr, tpr, label='ROC curve (area = %0.2f)' % roc_auc)
        pl.plot([0, 1], [0, 1], 'k--')
        pl.xlim([0.0, 1.0])
        pl.ylim([0.0, 1.0])
        pl.xlabel('False Positive Rate')
        pl.ylabel('True Positive Rate')
        pl.title('Receiver operating characteristic example')
        pl.legend(loc="lower right")
        pl.show()



#test
c = Control()
b = Backprop()

b.load_CSV('data_sets/new_iris_dataset.csv')
network = b.train(60, 90)
data_set = b.get_data_set(100)

# c.draw_confusion_matrix(network, data_set)
# print "Predict y:\n{}".format(c.y_predict)

#print b.get_data_set_by_levels(50)

if b.is_binary():
    c.draw_roc(network, data_set)
