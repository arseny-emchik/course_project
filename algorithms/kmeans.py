__author__ = 'belov'

from time import time
import numpy as np
import pylab as pl

from sklearn import metrics
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import scale

# import files
import _interface


# =======================================================
#           K-Means clustering algorithm
# =======================================================

class Kmeans(_interface.InterfaceML):

    __data = None
    __labels = None
    __n_samples = None
    __n_features = None
    __n_digits = None

    def __set_data(self):
        if len(self._data_set['target'][0]) != 1:
            return

        self.__data = self._data_set['input']
        self.__n_samples, __n_features = self.__data.shape
        self.__n_digits = len(np.unique(self._data_set['target']))
        self.__labels = np.ravel(self._data_set['target'])

    def train(self, init = "k-means++", n_init = 10):
        self.__set_data()
        km = KMeans(init=init, n_clusters=self.__n_digits, n_init=n_init)
        return km

    def printResult(self, estimator):
        t0 = time()
        data = self.__data
        estimator.fit(data)
        print('%.2fs    %i   %.3f   %.3f   %.3f   %.3f   %.3f   %.3f'
              % ((time() - t0), estimator.inertia_,
                 metrics.homogeneity_score(self.__labels, estimator.labels_),
                 metrics.completeness_score(self.__labels, estimator.labels_),
                 metrics.v_measure_score(self.__labels, estimator.labels_),
                 metrics.adjusted_rand_score(self.__labels, estimator.labels_),
                 metrics.adjusted_mutual_info_score(self.__labels,  estimator.labels_),
                 metrics.silhouette_score(data, estimator.labels_, metric='euclidean', sample_size=300)))

    def showPlot(self, km):
        reduced_data = PCA(n_components=2).fit_transform(self.__data)
        kmeans = km
        kmeans.fit(reduced_data)

        # Step size of the mesh. Decrease to increase the quality of the VQ.
        h = .02     # point in the mesh [x_min, m_max]x[y_min, y_max].

        # Plot the decision boundary. For that, we will assign a color to each
        x_min, x_max = reduced_data[:, 0].min() - 2, reduced_data[:, 0].max() + 2
        y_min, y_max = reduced_data[:, 1].min() - 2, reduced_data[:, 1].max() + 2
        xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

        # Obtain labels for each point in mesh. Use last trained model.
        Z = kmeans.predict(np.c_[xx.ravel(), yy.ravel()])

        # Put the result into a color plot
        Z = Z.reshape(xx.shape)
        pl.figure(1)
        pl.clf()
        pl.imshow(Z, interpolation='nearest',
                  extent=(xx.min(), xx.max(), yy.min(), yy.max()),
                  cmap=pl.cm.Paired,
                  aspect='auto', origin='lower')

        pl.plot(reduced_data[:, 0], reduced_data[:, 1], 'k.', markersize=2)
        # Plot the centroids as a white X
        centroids = kmeans.cluster_centers_
        pl.scatter(centroids[:, 0], centroids[:, 1],
                   marker='x', s=169, linewidths=3,
                   color='w', zorder=10)
        pl.title('K-means clustering on the digits dataset (PCA-reduced data)\n'
                 'Centroids are marked with white cross')
        pl.xlim(x_min, x_max)
        pl.ylim(y_min, y_max)
        pl.xticks(())
        pl.yticks(())
        pl.show()

_m = Kmeans()
train = _m.train
printResult = _m.printResult
showPlot = _m.showPlot

load_CSV = _m.load_CSV
get_data_set = _m.get_data_set
show_CSV = _m.show_CSV