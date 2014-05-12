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
    def train(self, m_quantile=0.15, m_cluster_all=True):
        self.__set_data()
        bandwidth = estimate_bandwidth(self.__data, quantile=m_quantile) #, n_samples=500


        ms = MeanShift(bandwidth=bandwidth, bin_seeding=True, cluster_all=m_cluster_all)
        ms.fit(self.__data)
        self.__labels = ms.labels_
        self.__cluster_centers = ms.cluster_centers_

        labels_unique = np.unique(self.__labels)
        self.__n_clusters = len(labels_unique)

        return ms

    def getResult(self):
        text = ('Estimated number of clusters: %d\n' % self.__n_clusters)
        text += ("Homogeneity: %0.3f\n" % metrics.homogeneity_score(self.__labels_true, self.__labels))
        text += ("Completeness: %0.3f\n" % metrics.completeness_score(self.__labels_true, self.__labels))
        text += ("V-measure: %0.3f\n" % metrics.v_measure_score(self.__labels_true, self.__labels))
        text += ("Adjusted Rand Index: %0.3f\n"
              % metrics.adjusted_rand_score(self.__labels_true, self.__labels))
        text += ("Adjusted Mutual Information: %0.3f\n"
              % metrics.adjusted_mutual_info_score(self.__labels_true, self.__labels))
        text += ("Silhouette Coefficient: %0.3f"
              % metrics.silhouette_score(self.__data, self.__labels))
        return text

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
getResult = _m.getResult
showPlot3D = _m.showPlot3D

load_CSV = _m.load_CSV
get_data_set = _m.get_data_set
show_CSV = _m.show_CSV

