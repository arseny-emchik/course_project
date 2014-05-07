# coding=utf-8
# =======================================================
#           IMPORTS
# =======================================================
import numpy as np
import pylab as pl
from sklearn.cluster import MeanShift, estimate_bandwidth
import mpl_toolkits.mplot3d.axes3d as p3
from sklearn import metrics

# import files
import _interface

# =======================================================
#           Mean-shift clustering algorithm
# =======================================================
class MSC(_interface.InterfaceML):

    __n_clusters = None
    __cluster_centers = None
    __data = None
    __labels = None
    __labels_true = None

    def __set_data(self):
        if len(self._data_set['target'][0]) != 1:
            return

        self.__data = np.array(self._data_set['input'])
        self.__labels_true = np.ravel(self._data_set['target'])

    # have to change the name of func train
    def train(self):
        self.__set_data()
        bandwidth = estimate_bandwidth(self.__data, quantile=0.15) #, n_samples=500


        ms = MeanShift(bandwidth=bandwidth, bin_seeding=True)
        ms.fit(self.__data)
        self.__labels = ms.labels_
        self.__cluster_centers = ms.cluster_centers_

        labels_unique = np.unique(self.__labels)
        self.__n_clusters = len(labels_unique)

        return ms

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

    def showPlot3D(self):
        fig = pl.figure()
        ax = p3.Axes3D(fig)
        ax.view_init(7, -80)
        for l in np.unique(self.__labels):
            ax.plot3D(self.__data[self.__labels == l, 0], self.__data[self.__labels == l, 1], self.__data[self.__labels == l, 2],
                      'o', color=pl.cm.jet(float(l) / np.max(self.__labels + 1)))

        pl.title("Number of estimated clusters : %d" % self.__n_clusters)
        pl.show()

_m = MSC()
train = _m.train
printResult = _m.printResult
showPlot3D = _m.showPlot3D

load_CSV = _m.load_CSV
get_data_set = _m.get_data_set
show_CSV = _m.show_CSV

