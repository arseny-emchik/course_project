# coding=utf-8
# =======================================================
#           IMPORTS
# =======================================================
from pybrain.supervised.trainers import BackpropTrainer
from sklearn.metrics import classification_report

import _interface
import control

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
        return classification_report(y_true, y_predict)

_b = Backprop()
train = _b.train
getResult = _b.getResult

load_CSV = _b.load_CSV
get_data_set = _b.get_data_set
show_CSV = _b.show_CSV
is_binary = _b.is_binary