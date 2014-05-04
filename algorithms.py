# coding=utf-8
# =======================================================
#           IMPORTS
# =======================================================
from abc import ABCMeta, abstractmethod, abstractproperty
import csv
import numpy as np

from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.structure import TanhLayer
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.supervised.trainers import RPropMinusTrainer

from sklearn.metrics import confusion_matrix, roc_curve, auc
from sklearn.tree import DecisionTreeClassifier
from sklearn import svm

import pylab as pl
from random import randint
# =======================================================

# =======================================================
#          Classifier Interface
# =======================================================
class InterfaceClassifier:
    __metaclass__ = ABCMeta

    # private class variables
    __hFile = None
    __csv_file = None
    __row_count = None
    __binary = False
    __data_set = None

    # private class methods
    def __get_full_data_set(self, num_inputs=-1, num_outputs=1):
        num_inputs = self._count_inputs() if num_inputs == -1 else num_inputs
        if num_inputs <= 0 or num_outputs <= 0:
            return

        self.__data_set = SupervisedDataSet(num_inputs, num_outputs)
        self.hFile.seek(0)
        for row in self.csv_file:
            indata = row[:num_inputs]
            outdata = row[num_inputs:]
            self.__data_set.addSample(indata, outdata)
        return self.__data_set

    def __get_levels(self):
        levels = []
        for i in self.__data_set['target']:
            level = int(i)
            if level not in levels:
                levels.append(level)
        return levels

    def __get_data_set_array_with_specific_level(self, level):
        result = []
        for i in self.__data_set:
            current_level = int(i[1])
            if current_level == level:
                result.append(i)
        return result

    # protected class methods
    def _count_inputs(self, number_inputs=-1):
        self.hFile.seek(0)
        for row in self.csv_file:
            return len(row) - 1 if number_inputs == -1 else number_inputs
        return 0

    def _buildNet(self, hidden_layers, num_outputs, num_inputs, hiddenclass):
        return buildNetwork(num_inputs, hidden_layers, num_outputs)

    # public class methods
    def load_CSV(self, file_name):
        self.hFile = open(file_name, 'rb')
        self.csv_file = csv.reader(self.hFile)
        self.row_count = sum(1 for row in self.csv_file)
        self.__data_set = self.__get_full_data_set()

        if len(self.__get_levels()) == 2:
            self.binary = True

        return self.csv_file

    # test method
    def show_CSV(self):
        self.hFile.seek(0)
        for row in self.csv_file:
            print row

    def is_binary(self):
        return self.__binary

    def get_data_set(self, percent, num_inputs=-1, num_outputs=1):
        num_inputs = self._count_inputs() if num_inputs == -1 else num_inputs
        if num_inputs <= 0 or num_outputs <= 0 or percent <= 0 or percent > 100:
            return

        if percent == 100:
            return self.__data_set

        levels = self.__get_levels()
        ds = SupervisedDataSet(num_inputs, num_outputs)
        num_rows = int(self.row_count * (float(percent) / 100.0))
        num_rows_in_class = int(num_rows / len(levels))

        for level in levels:
            data_set = self.__get_data_set_array_with_specific_level(level)
            used_samples = []
            for i in range(num_rows_in_class):
                added = False
                while (not added):
                    row = randint(0, num_rows_in_class)
                    if row not in used_samples:
                        used_samples.append(row)
                        sample = data_set[row]
                        ds.addSample(sample[0], sample[1])
                        added = True
        return ds

    # abstract methods
    @abstractmethod
    def train(self,
              cycles,
              percent,
              hidden_layers=3,
              num_outputs=1,
              num_inputs=-1,
              hiddenclass=None):
        """train net
        :param cycles:
        :param percent:
        :param hidden_layers:
        :param num_outputs:
        :param num_inputs:
        :param hiddenclass:
        """

# =======================================================
#           Algorithms
# =======================================================

# =======================================================
#           Back propagation
# =======================================================
class Backprop(InterfaceClassifier):
    def train(self,
              cycles,
              percent,
              hidden_layers=3,
              num_outputs=1,
              num_inputs=-1,
              hiddenclass=None):
        num_inputs = self._count_inputs() if num_inputs == -1 else num_inputs
        if num_inputs <= 0 or num_outputs <= 0 or cycles <= 0 or (percent > 100 or percent <= 0):
            return

        network = self._buildNet(hidden_layers, num_outputs, num_inputs, hiddenclass)
        data_set = self.get_data_set(percent, num_inputs, num_outputs)
        trainer = BackpropTrainer(network, data_set)

        for i in range(cycles):
            trainer.train()

        return network

# =======================================================
#           Resilient propagation
# =======================================================
class Rprop(InterfaceClassifier):
    def train(self,
              cycles,
              percent,
              hidden_layers=3,
              num_outputs=1,
              num_inputs=-1,
              hiddenclass=None):
        num_inputs = self._count_inputs() if num_inputs == -1 else num_inputs
        if num_inputs <= 0 or num_outputs <= 0 or cycles <= 0 or (percent > 100 or percent <= 0):
            return

        network = self._buildNet(hidden_layers, num_outputs, num_inputs, hiddenclass)
        data_set = self.get_data_set(percent, num_inputs, num_outputs)

        trainer = RPropMinusTrainer(network, dataset=data_set)

        for i in range(cycles):
            trainer.train()

        return network

# =======================================================
#           Decision Tree
# =======================================================
class DTree(InterfaceClassifier):
    def train(self,
              percent,
              num_outputs=1,
              num_inputs=-1,
              hiddenclass=None):
        num_inputs = self._count_inputs() if num_inputs == -1 else num_inputs
        data_set = self.get_data_set(percent, num_inputs, num_outputs)
        clf = DecisionTreeClassifier().fit(data_set['input'], data_set['target'])

        return clf

# =======================================================
#           Support Vector Machines
# =======================================================
class SVM(InterfaceClassifier):
    def train(self,
              percent,
              num_outputs=1,
              num_inputs=-1,
              hiddenclass=None):
        num_inputs = self._count_inputs() if num_inputs == -1 else num_inputs
        data_set = self.get_data_set(percent, num_inputs, num_outputs)
        clf = svm.SVC().fit(data_set['input'], np.ravel(data_set['target']))

        return clf

# =======================================================
#           CONTROL
# =======================================================
class Control:
    # private class methods
    def __calculate_entire_ds(self, function, data_set):
        y_true = []
        y_predict = []

        for i in data_set:
            predict = int(round(function(i[0])))
            true = int(i[1][0])
            y_predict.append(predict)
            y_true.append(true)

        # print "{} {}".format(predict,true)
        # print y_true
        # print y_predict
        return y_true, y_predict

    # public methods
    def draw_confusion_matrix(self, function, data_set):
        y_true, y_predict = self.__calculate_entire_ds(function, data_set)
        cm = confusion_matrix(y_true, y_predict)
        pl.matshow(cm)
        pl.title('Confusion matrix')
        pl.colorbar()
        pl.ylabel('True label')
        pl.xlabel('Predicted label')
        pl.show()

    def draw_roc(self, function, data_set):
        y_true, y_predict = self.__calculate_entire_ds(function, data_set)
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


# tested 04.05.14 by ars & alex =)
c = Control()

# #test 1
# b = Backprop()
# b.load_CSV('data_sets/new_iris_dataset.csv')
# network = b.train(60, 90)
# data_set = b.get_data_set(100)
# c.draw_confusion_matrix(network.activate, data_set)
#
# c.draw_confusion_matrix(network, data_set)
#
# #test 2
# d = DTree()
# d.load_CSV('data_sets/new_iris_dataset.csv')
# network = d.train(90)
# data_set = d.get_data_set(100)
#
# #c.draw_confusion_matrix(network, data_set)
#
# # test 3
# r = Rprop()
# d.load_CSV('data_sets/new_iris_dataset.csv')
# network = d.train(60, 90)
# data_set = d.get_data_set(100)
#
# #c.draw_confusion_matrix(network, data_set)

#test 4
d = SVM()
d.load_CSV('data_sets/new_iris_dataset.csv')
clf = d.train(90)
data_set = d.get_data_set(100)
c.draw_confusion_matrix(clf.predict, data_set)
data_set = d.get_data_set(100)
