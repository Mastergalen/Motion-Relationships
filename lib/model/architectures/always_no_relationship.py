"""
Always no relationship baseline
"""
import numpy as np
import matplotlib.pyplot as plt

from lib.model.loaders.kinetics_bottleneck import KineticsBottleneckLoader
from lib.model import evaluation

_NB_CLASSES = 4


def main():
    data = KineticsBottleneckLoader(_NB_CLASSES, 'test')
    x, y = data.load_all()

    y_pred = np.zeros(len(y))
    y_pred[:] = 0  # Always predict no relationship

    evaluation.draw_confusion_matrix(np.argmax(y, axis=1), y_pred)

    plt.show()


if __name__ == '__main__':
    main()
