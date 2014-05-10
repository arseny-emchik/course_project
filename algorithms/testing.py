# coding=utf-8
# =======================================================
#           IMPORTS
# =======================================================
#import files
import back_propagation
import DBScan
import decision_tree
import mshift
import resilient_propagation
import support_vector
import control


# #test 1
# back_propagation.load_CSV('../data_sets/binary_iris_dataset.csv')
# network = back_propagation.train(60, 90)
# data_set = back_propagation.get_data_set(100)
# control.draw_roc(network.activate, data_set)

# #test 2
# decision_tree.load_CSV('../data_sets/new_iris_dataset.csv')
# clf = decision_tree.train(90, max_features="log2")
# data_set = decision_tree.get_data_set(100)
# control.draw_confusion_matrix(clf.predict, data_set)
#
# # test 3
# resilient_propagation.load_CSV('../data_sets/new_iris_dataset.csv')
# network = resilient_propagation.train(60, 90)
# data_set = resilient_propagation.get_data_set(100)
#
# #test 4
# support_vector.load_CSV('../data_sets/new_iris_dataset.csv')
# clf = support_vector.train(90, kernel="rbf")
# data_set = support_vector.get_data_set(100)
# control.draw_confusion_matrix(clf.predict, data_set)
# data_set = support_vector.get_data_set(100)

# #test 5
# mshift.load_CSV('../data_sets/new_iris_dataset.csv')
# mean_shift = mshift.train()
# mshift.show_CSV()
# data_set = mshift.get_data_set(100)
# mshift.printResult()
#
# mshift.showPlot3D()
#
# DBScan.load_CSV('../data_sets/new_iris_dataset.csv')
# DBScan.train()
# DBScan.showPlot2D()
# DBScan.showPlot3D()
# DBScan.printResult()
