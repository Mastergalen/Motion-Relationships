import numpy as np
from sklearn.metrics import confusion_matrix
from sklearn.metrics import f1_score


def evaluate(trained_model, x_test, y_test):
    y_pred = np.argmax(trained_model.predict(x_test), axis=1)
    y_true = np.argmax(y_test, axis=1)
    draw_cf_matrix(y_true, y_pred)


def draw_cf_matrix(y_true, y_pred):
    cf_matrix = confusion_matrix(y_true, y_pred)
    print(cf_matrix)

    class_wise_f1 = np.round(f1_score(y_true, y_pred, average=None)*100)*0.01
    f_score = np.mean(class_wise_f1)

    print('the mean-f1 score: {:.2f}'.format(f_score))