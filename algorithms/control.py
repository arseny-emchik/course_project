# coding=utf-8
# module control
# =======================================================
#           IMPORTS
# =======================================================
import pylab as pl
from sklearn.metrics import confusion_matrix, roc_curve, auc


# =======================================================
#           CONTROL
# =======================================================
class Control:
    # public methods
    def calculate_entire_ds(self, function, data_set):
        y_true = []
        y_predict = []

        for i in data_set:
            predict = int(round(function(i[0])))
            true = int(i[1][0])
            y_predict.append(predict)
            y_true.append(true)

        # print "{} {}".format(predict,true)
        # print y_true
        # print y_predict
        return y_true, y_predict

    def draw_confusion_matrix(self, function, data_set):
        y_true, y_predict = self.calculate_entire_ds(function, data_set)
        cm = confusion_matrix(y_true, y_predict)
        pl.matshow(cm)
        pl.title('Confusion matrix')
        pl.colorbar()
        pl.ylabel('True label')
        pl.xlabel('Predicted label')
        pl.show()

    def draw_roc(self, function, data_set):
        y_true, y_predict = self.calculate_entire_ds(function, data_set)
        # print y_true
        # print y_predict
        fpr, tpr, thresholds = roc_curve(y_true, y_predict)
        roc_auc = auc(fpr, tpr)
        print("Area under the ROC curve : %f" % roc_auc)

        # Plot ROC curve
        pl.clf()
        pl.plot(fpr, tpr, label='ROC curve (area = %0.2f)' % roc_auc)
        pl.plot([0, 1], [0, 1], 'k--')
        pl.xlim([0.0, 1.0])
        pl.ylim([0.0, 1.0])
        pl.xlabel('False Positive Rate')
        pl.ylabel('True Positive Rate')
        pl.title('Receiver operating characteristic example')
        pl.legend(loc="lower right")
        pl.show()

_control = Control()
draw_confusion_matrix = _control.draw_confusion_matrix
draw_roc = _control.draw_roc
calculate_entire_ds = _control.calculate_entire_ds
