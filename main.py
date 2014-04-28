# ====================================================
#                     imports
# ====================================================
#import pybrain
from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
from pybrain.structure import TanhLayer
from pybrain.supervised.trainers import BackpropTrainer
# ====================================================


#test 1
# ====================================================
net = buildNetwork(2, 3, 1)
net.activate([2, 1])
print net['in']
# ====================================================


#test 2  XOR
# ====================================================
ds = SupervisedDataSet(2, 1)
ds.addSample((0, 0), (0,))
ds.addSample((0, 1), (1,))
ds.addSample((1, 0), (1,))
ds.addSample((1, 1), (0,))

print ds['input']
print ds['target']
# ====================================================


#test 3
# ====================================================
net = buildNetwork(2, 3, 1, bias=True, hiddenclass=TanhLayer)
trainer = BackpropTrainer(net, ds)
print trainer.train()
# ====================================================


# NOTE some useful func
# ====================================================
# ds = SequentialDataSet.loadFromFile('some_file.csv')
# ====================================================




