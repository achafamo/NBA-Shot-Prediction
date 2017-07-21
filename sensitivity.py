import math
from sklearn import metrics
from rating_create import *
import matplotlib.pyplot as plt


def y_predicted(threshold, prob_predictions, class_labels):
    return [class_labels[math.ceil(prob)-threshold] for prob in prob_predictions]

def ROCurve():
    '''
    This is the measure of the Recieving operator characterstics
    '''

    x_train, y_train, x_test, y_test = load_data()
    predictions = classify()
    new_predictions = []
    for prediction in predictions:
        new_predictions.append(prediction[0])

    fpr, tpr, thresholds = metrics.roc_curve(y_test, new_predictions, pos_label='made')
    plot_auc(fpr,tpr)
    #return fpr, tpr


def plot_auc(false_rate,true_rate):

    plt.plot(false_rate,true_rate)
    plt.plot([0, 1], [0, 1], linestyle='--', lw=2, color='k',label='Luck')
    plt.xlim([-0.05, 1.05])
    plt.ylim([-0.05, 1.05])
    plt.title('Sensitivity, ROC Curve')
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positve Rate')
    plt.legend(loc="lower right")
    plt.show()
    #plt.show()