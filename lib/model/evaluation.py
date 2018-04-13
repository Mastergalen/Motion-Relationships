import numpy as np
from sklearn.metrics import confusion_matrix
from sklearn.metrics import f1_score


def evaluate_generator(trained_model, generator):
    y_pred = np.argmax(trained_model.predict_generator(generator), axis=1)
    y_true = generator.classes
    cf_matrix = confusion_matrix(y_true, y_pred)
    print(cf_matrix)

    class_wise_f1 = np.round(f1_score(y_true, y_pred, average=None)*100)*0.01
    f_score = np.mean(class_wise_f1)

    print('the mean-f1 score: {:.2f}'.format(f_score))


def evaluate(trained_model, x, y):
    y_pred = np.argmax(trained_model.predict_generator(x), axis=1)
    y_true = y
    cf_matrix = confusion_matrix(y_true, y_pred)
    print(cf_matrix)

    class_wise_f1 = np.round(f1_score(y_true, y_pred, average=None) * 100) * 0.01
    f_score = np.mean(class_wise_f1)

    print('the mean-f1 score: {:.2f}'.format(f_score))