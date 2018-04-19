import numpy as np
import matplotlib.pyplot as plt
import itertools
from sklearn.metrics import confusion_matrix
from sklearn.metrics import f1_score


def evaluate(trained_model, x_test, y_test):
    y_pred = np.argmax(trained_model.predict(x_test), axis=1)
    y_true = np.argmax(y_test, axis=1)
    cf_matrix = confusion_matrix(y_true, y_pred)

    f, (ax1, ax2) = plt.subplots(1, 2)
    classes = ['No relationship', 'Avoids', 'Gives-way', 'Group']
    plot_confusion_matrix(cf_matrix, axes=ax1, title='Without normalisation', classes=classes)
    plot_confusion_matrix(cf_matrix, axes=ax2, title='Normalisation', normalize=True, classes=classes)


def plot_confusion_matrix(cm, classes, axes,
                          normalize=False,
                          title='Confusion matrix',
                          cmap=plt.cm.get_cmap("Blues")):
    """
    This function prints and plots the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]

    plt.sca(axes)
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title)
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes, rotation=45)
    plt.yticks(tick_marks, classes)

    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        axes.text(j, i, format(cm[i, j], fmt),
                  horizontalalignment="center",
                  color="white" if cm[i, j] > thresh else "black")

    plt.tight_layout()
    plt.ylabel('True label')
    plt.xlabel('Predicted label')