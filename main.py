# ====================================================
#                     imports
# ====================================================
#import pybrain
from pybrain.tools.shortcuts import buildNetwork
from pybrain.datasets import SupervisedDataSet
# ====================================================


net = buildNetwork(2, 3, 1)
print net['in']