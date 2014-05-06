# coding=utf-8
# =======================================================
#           IMPORTS
# =======================================================
from abc import ABCMeta, abstractmethod, abstractproperty
import csv
import numpy as np
import pylab as pl
from random import randint

from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet

from pybrain.supervised.trainers import BackpropTrainer
from pybrain.supervised.trainers import RPropMinusTrainer

from sklearn.tree import DecisionTreeClassifier
from sklearn import svm

#metrics for classification
from sklearn.metrics import confusion_matrix, roc_curve, auc

# for clustering
from sklearn.cluster import MeanShift, estimate_bandwidth
from itertools import cycle
import mpl_toolkits.mplot3d.axes3d as p3

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN

#metrics for clustering
from sklearn import metrics
# =======================================================

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
            self.binary = True

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
class Backprop(InterfaceML):
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
class Rprop(InterfaceML):
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
class DTree(InterfaceML):
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
class SVM(InterfaceML):
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
#           Mean-shift clustering algorithm
# =======================================================
class MSC(InterfaceML):

    __n_clusters = None
    __cluster_centers = None
    __data = None
    __labels = None

    def __set_data(self, n_inputs):
        if self._count_inputs < n_inputs or n_inputs < 1:
            return

        arr_rows = []
        self._hFile.seek(0)

        for row in self._csv_file:
            arr = [float(x) for x in row[:n_inputs]]
            arr_rows.append(arr)

        self.__data = np.array(arr_rows)

    # have to change the name of func train
    def train(self, n_inputs):
        self.__set_data(n_inputs)
        bandwidth = estimate_bandwidth(self.__data, quantile=0.15) #, n_samples=500

        ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
        ms.fit(self.__data)
        self.__labels = ms.labels_
        self.__cluster_centers = ms.cluster_centers_

        labels_unique = np.unique(self.__labels)
        self.__n_clusters = len(labels_unique)

        return ms

    def showPlot(self):
        fig = pl.figure()
        ax = p3.Axes3D(fig)
        ax.view_init(7, -80)
        for l in np.unique(self.__labels):
            ax.plot3D(self.__data[self.__labels == l, 0], self.__data[self.__labels == l, 1], self.__data[self.__labels == l, 2],
                      'o', color=pl.cm.jet(float(l) / np.max(self.__labels + 1)))

        pl.title("Number of estimated clusters : %d" % self.__n_clusters)
        pl.show()

# =======================================================
#           DBSCAN clustering algorithm
# =======================================================
class DBScanC(InterfaceML):

    __n_clusters = None
    __cluster_centers = None
    __data = None
    __labels = None
    __labels_true = None
    __core_samples = None

    def __set_data(self, n_inputs):
        if self._count_inputs < n_inputs or n_inputs < 1:
            return

        arr_data = []
        for row in self._data_set['input']:
            arr_data.append(row[:n_inputs])

        self.__data = np.array(arr_data)
        a = np.ravel(self._data_set['target'])
        self.__labels_true = np.ravel(self._data_set['target'])
        self.__data = StandardScaler().fit_transform(self.__data)

    def train(self, n_inputs):
        self.__set_data(n_inputs)

        db = DBSCAN(eps=0.4, min_samples=10).fit(self.__data)
        self.__core_samples = db.core_sample_indices_
        self.__labels = db.labels_

        self.__n_clusters = len(set(self.__labels)) - (1 if -1 in self.__labels else 0)

        print('Estimated number of clusters: %d' % self.__n_clusters)
        print("Homogeneity: %0.3f" % metrics.homogeneity_score(self.__labels_true, self.__labels))
        print("Completeness: %0.3f" % metrics.completeness_score(self.__labels_true, self.__labels))
        print("V-measure: %0.3f" % metrics.v_measure_score(self.__labels_true, self.__labels))
        print("Adjusted Rand Index: %0.3f"
              % metrics.adjusted_rand_score(self.__labels_true, self.__labels))
        print("Adjusted Mutual Information: %0.3f"
              % metrics.adjusted_mutual_info_score(self.__labels_true, self.__labels))
        print("Silhouette Coefficient: %0.3f"
              % metrics.silhouette_score(self.__data, self.__labels))

    def showPlot(self):
        unique_labels = set(self.__labels)
        colors = pl.cm.Spectral(np.linspace(0, 1, len(unique_labels)))
        for k, col in zip(unique_labels, colors):
            if k == -1:
                # Black used for noise.
                col = 'k'
                markersize = 6
            class_members = [index[0] for index in np.argwhere(self.__labels == k)]
            cluster_core_samples = [index for index in self.__core_samples
                                    if self.__labels[index] == k]
            for index in class_members:
                x = self.__data[index]
                if index in self.__core_samples and k != -1:
                    markersize = 14
                else:
                    markersize = 6
                pl.plot(x[0], x[1], 'o', markerfacecolor=col,
                        markeredgecolor='k', markersize=markersize)

        pl.title('Estimated number of clusters: %d' % self.__n_clusters)
        pl.show()








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
        # print y_true
        # print y_predict
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

#test 1
b = Backprop()
b.load_CSV('data_sets/binary_iris_dataset.csv')
network = b.train(60, 90)
data_set = b.get_data_set(100)
c.draw_roc(network.activate, data_set)
#c.draw_confusion_matrix(network.activate, data_set)

#test 2
d = DTree()
d.load_CSV('data_sets/new_iris_dataset.csv')
clf = d.train(90)
data_set = d.get_data_set(100)
c.draw_confusion_matrix(clf.predict, data_set)
#
# # test 3
# r = Rprop()
# d.load_CSV('data_sets/new_iris_dataset.csv')
# network = d.train(60, 90)
# data_set = d.get_data_set(100)
#
# #c.draw_confusion_matrix(network, data_set)

# #test 4
# d = SVM()
# d.load_CSV('data_sets/new_iris_dataset.csv')
# clf = d.train(90)
# data_set = d.get_data_set(100)
# c.draw_confusion_matrix(clf.predict, data_set)
# data_set = d.get_data_set(100)

#test 5
m = MSC()
m.load_CSV('data_sets/new_iris_dataset.csv')
ms = m.train(3) # n_inputs have to move into load_CSV
data_set = m.get_data_set(100)
labels_true = np.ravel(data_set['target'].astype(np.int))
labels_predict = ms.labels_.astype(np.int)
print metrics.completeness_score(labels_true, labels_predict)
print metrics.homogeneity_score(labels_true, labels_predict)
print metrics.mutual_info_score(labels_true, labels_predict)
m.showPlot()

s = DBScanC()
s.load_CSV('data_sets/new_iris_dataset.csv')
s.train(2)
s.showPlot()