# coding=utf-8
# =======================================================
#           IMPORTS
# =======================================================
import numpy as np
from sklearn import svm

import _interface
# =======================================================
#           Support Vector Machines
# =======================================================
class SVM(_interface.InterfaceML):
    def train(self,
              percent,
              num_outputs=1,
              num_inputs=-1,
              hiddenclass=None):
        num_inputs = self._count_inputs() if num_inputs == -1 else num_inputs
        data_set = self.get_data_set(percent, num_inputs, num_outputs)
        clf = svm.SVC().fit(data_set['input'], np.ravel(data_set['target']))

        return clf

_s = SVM()
train = _s.train

load_CSV = _s.load_CSV
get_data_set = _s.get_data_set
show_CSV = _s.show_CSV