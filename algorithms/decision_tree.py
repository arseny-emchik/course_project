# coding=utf-8
# =======================================================
#           IMPORTS
# =======================================================
from sklearn.tree import DecisionTreeClassifier
import _interface

# =======================================================
#           Decision Tree
# =======================================================
class DTree(_interface.InterfaceML):
    def train(self,
              percent,
              num_outputs=1,
              num_inputs=-1,
              hiddenclass=None):
        num_inputs = self._count_inputs() if num_inputs == -1 else num_inputs
        data_set = self.get_data_set(percent, num_inputs, num_outputs)
        clf = DecisionTreeClassifier().fit(data_set['input'], data_set['target'])

        return clf


_d = DTree()
train = _d.train

load_CSV = _d.load_CSV
get_data_set = _d.get_data_set
show_CSV = _d.show_CSV