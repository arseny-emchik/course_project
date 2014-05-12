# coding=utf-8
# =======================================================
#           IMPORTS
# =======================================================
from pybrain.supervised.trainers import BackpropTrainer

import _interface
import control
import sklearn.metrics as metrics

# =======================================================
#           Back propagation
# =======================================================
class Backprop(_interface.InterfaceML):
    def train(self,
              cycles,
              percent,
              hidden_layers=3,
              hiddenclass=None,
              num_outputs=1,
              num_inputs=-1):
        num_inputs = self._count_inputs() if num_inputs == -1 else num_inputs
        if num_inputs <= 0 or num_outputs <= 0 or cycles <= 0 or (percent > 100 or percent <= 0):
            return

        network = self._buildNet(hidden_layers, num_outputs, num_inputs, hiddenclass)
        data_set = self.get_data_set(percent, num_inputs, num_outputs)
        trainer = BackpropTrainer(network, data_set)

        for i in range(cycles):
            trainer.train()

        return network

    def getResult(self, network, data_set):
        y_true, y_predict = control.calculate_entire_ds(network.activate, data_set)
        result = metrics.classification_report(y_true, y_predict)
        result += "\n Accuracy: %f\n" % metrics.accuracy_score(y_true, y_predict)
        result += "Average precision: %f\n" % metrics.average_precision_score(y_true, y_predict)
        result += "F1 score: %f\n" % metrics.f1_score(y_true, y_predict)
        result += "Fbeta score: %f\n" % metrics.fbeta_score(y_true, y_predict)
        result += "Hamming loss: %f\n" % metrics.hamming_loss(y_true, y_predict)
        result += "Hinge loss: %f\n" % metrics.hinge_loss(y_true, y_predict)
        result += "Jaccard similarity: %f\n" % metrics.jaccard_similarity_score(y_true, y_predict)
        result += "Logistic loss: %f\n" % metrics.log_loss(y_true, y_predict)
        result += "Matthews correlation coefficient: %f\n" % metrics.matthews_corrcoef(y_true, y_predict)
        result += "Precision: %f\n" % metrics.precision_score(y_true, y_predict)
        result += "Recall: %f\n" % metrics.recall_score(y_true, y_predict)
        result += "Area Under the Curve: %f\n" % metrics.roc_auc_score(y_true, y_predict)
        return result

_b = Backprop()
train = _b.train
getResult = _b.getResult

load_CSV = _b.load_CSV
get_data_set = _b.get_data_set
show_CSV = _b.show_CSV
is_binary = _b.is_binary