# coding=utf-8
# =======================================================
#           IMPORTS
# =======================================================
import numpy as np
import pylab as pl
import mpl_toolkits.mplot3d.axes3d as p3

from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN
from sklearn import metrics

# import files
import _interface

# =======================================================
#           DBSCAN clustering algorithm
# =======================================================
class DBScanC(_interface.InterfaceML):

    __n_clusters = None
    __cluster_centers = None
    __data = None
    __labels = None
    __labels_true = None
    __core_samples = None

    def __set_data(self):
        if len(self._data_set['target'][0]) != 1:
            return

        self.__data = np.array(self._data_set['input'])
        self.__data = StandardScaler().fit_transform(self.__data)

        self.__labels_true = np.ravel(self._data_set['target'])

    def train(self):
        self.__set_data()

        db = DBSCAN(eps=0.4, min_samples=10).fit(self.__data)
        self.__core_samples = db.core_sample_indices_
        self.__labels = db.labels_

        self.__n_clusters = len(set(self.__labels)) - (1 if -1 in self.__labels else 0)

    def printResult(self):
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



        # labels_true = np.ravel(data_set['target'].astype(np.int))
        # labels_predict = ms.labels_.astype(np.int)
        # print metrics.completeness_score(labels_true, labels_predict)
        # print metrics.homogeneity_score(labels_true, labels_predict)
        # print metrics.mutual_info_score(labels_true, labels_predict)

    def showPlot2D(self):
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

    def showPlot3D(self):

        fig = pl.figure()
        ax = p3.Axes3D(fig)
        ax.view_init(7, -80)
        for l in np.unique(self.__labels):
            ax.plot3D(self.__data[self.__labels == l, 0], self.__data[self.__labels == l, 1], self.__data[self.__labels == l, 2],
                      'o', color=pl.cm.jet(float(l) / np.max(self.__labels + 1)))

        pl.title("Number of estimated clusters : %d" % self.__n_clusters)
        pl.show()

_d = DBScanC()
train = _d.train
printResult = _d.printResult
showPlot2D = _d.showPlot2D
showPlot3D = _d.showPlot3D

load_CSV = _d.load_CSV
get_data_set = _d.get_data_set
show_CSV = _d.show_CSV


