# coding=utf-8
# module _interface
# =======================================================
#           IMPORTS
# =======================================================
from abc import ABCMeta, abstractmethod
import csv
from random import randint
from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
import control
import sklearn.metrics as metrics

# =======================================================
#          Classifier Interface
# =======================================================


class InterfaceML:
    __metaclass__ = ABCMeta

    # private class variables
    __row_count = None
    __binary = False

    _data_set = None
    _csv_file = None
    _hFile = None

    # private class methods
    def __get_full_data_set(self, num_inputs=-1, num_outputs=1):
        num_inputs = self._count_inputs() if num_inputs == -1 else num_inputs
        if num_inputs <= 0 or num_outputs <= 0:
            return

        self.__data_set = SupervisedDataSet(num_inputs, num_outputs)
        self._hFile.seek(0)
        for row in self._csv_file:
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
        self._hFile.seek(0)
        for row in self._csv_file:
            return len(row) - 1 if number_inputs == -1 else number_inputs
        return 0

    def _buildNet(self, hidden_layers, num_outputs, num_inputs, hiddenclass):
        return buildNetwork(num_inputs, hidden_layers, num_outputs)

    # public class methods
    def load_CSV(self, file_name):
        self._hFile = open(file_name, 'rb')
        self._csv_file = csv.reader(self._hFile)
        self.row_count = sum(1 for row in self._csv_file)
        self._data_set = self.__get_full_data_set()

        if len(self.__get_levels()) == 2:
            self.__binary = True

        return self._csv_file

    # test method
    def show_CSV(self):
        self._hFile.seek(0)
        for row in self._csv_file:
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

    def getResult(self, predict, data_set):
        y_true, y_predict = control.calculate_entire_ds(predict, data_set)
        result = metrics.classification_report(y_true, y_predict)
        result += "\nAccuracy classification: %f\n" % metrics.accuracy_score(y_true, y_predict)
        result += "F1 score: %f\n" % metrics.f1_score(y_true, y_predict)
        result += "Fbeta score: %f\n" % metrics.fbeta_score(y_true, y_predict, beta=0.5)
        result += "Hamming loss: %f\n" % metrics.hamming_loss(y_true, y_predict)
        result += "Hinge loss: %f\n" % metrics.hinge_loss(y_true, y_predict)
        result += "Jaccard similarity: %f\n" % metrics.jaccard_similarity_score(y_true, y_predict)
        result += "Precision: %f\n" % metrics.precision_score(y_true, y_predict)
        result += "Recall: %f\n" % metrics.recall_score(y_true, y_predict)

        if self.is_binary():
            result += "Average precision: %f\n" % metrics.average_precision_score(y_true, y_predict)
            result += "Matthews correlation coefficient: %f\n" % metrics.matthews_corrcoef(y_true, y_predict)
            result += "Area Under the Curve: %f\n" % metrics.roc_auc_score(y_true, y_predict)

        return result

    # abstract methods
    @abstractmethod
    def train(self,
              cycles,
              percent,
              hidden_layers=3,
              hiddenclass=None,
              num_outputs=1,
              num_inputs=-1):
        """train net
        :param cycles:
        :param percent:
        :param hidden_layers:
        :param num_outputs:
        :param num_inputs:
        :param hiddenclass:
        """

