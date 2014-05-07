# coding=utf-8
# =======================================================
#           IMPORTS
# =======================================================
from pybrain.supervised.trainers import RPropMinusTrainer
import _interface

# =======================================================
#           Resilient propagation
# =======================================================
class Rprop(_interface.InterfaceML):
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

_rp = Rprop()
train = _rp.train

load_CSV = _rp.load_CSV
get_data_set = _rp.get_data_set
show_CSV = _rp.show_CSV
