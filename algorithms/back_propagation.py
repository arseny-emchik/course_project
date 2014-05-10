# coding=utf-8
# =======================================================
#           IMPORTS
# =======================================================
from pybrain.supervised.trainers import BackpropTrainer
from pybrain.structure import LinearLayer, SigmoidLayer, GaussianLayer, LSTMLayer
from pybrain.structure import MDLSTMLayer, SoftmaxLayer, StateDependentLayer, TanhLayer
import _interface

# =======================================================
#           Back propagation
# =======================================================
class Backprop(_interface.InterfaceML):
    def train(self,
              cycles,
              percent,
              hidden_layers=3,
              num_outputs=1,
              num_inputs=-1,
              hiddenclass="TanhLayer"):
        num_inputs = self._count_inputs() if num_inputs == -1 else num_inputs
        if num_inputs <= 0 or num_outputs <= 0 or cycles <= 0 or (percent > 100 or percent <= 0):
            return

        network = self._buildNet(hidden_layers, num_outputs, num_inputs, hiddenclass)
        data_set = self.get_data_set(percent, num_inputs, num_outputs)
        trainer = BackpropTrainer(network, data_set)

        for i in range(cycles):
            trainer.train()

        return network

_b = Backprop()
train = _b.train

load_CSV = _b.load_CSV
get_data_set = _b.get_data_set
show_CSV = _b.show_CSV