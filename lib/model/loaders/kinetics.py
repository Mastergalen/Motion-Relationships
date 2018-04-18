import numpy as np
import os
import json
from random import shuffle

from lib.model.loaders import helpers

_DATA_DIR = 'data/kinetics'


class KineticsLoader:
    def __init__(self, batch_size, nb_classes):
        self.batch_size = batch_size
        self.step = 0
        self.nb_classes = nb_classes
        self.clips_to_label = []

        self.load_data()

    def next_batch(self):
        batch_x = np.zeros((self.batch_size, 150, 224, 224, 3))
        batch_y = np.zeros((self.batch_size, self.nb_classes))

        # FIXME: 2 of each class in each batch of 8
        for i in range(self.batch_size):
            clip_id, label = self.clips_to_label[self.step * self.batch_size + i]
            batch_x[i, ...] = np.load(os.path.join(_DATA_DIR, 'rgb_{}.npy'.format(clip_id)))
            batch_y[i, label] = 1

        self.step += 1

        return batch_x, batch_y

    def load_data(self):
        """
        (clip_id, class_id)
        :return:
        """
        label_paths = helpers.list_labels()

        for path in label_paths:
            clip_id = os.path.splitext(os.path.basename(path))[0]
            labels = np.array(json.load(open(path)))

            for idx, label in np.ndenumerate(labels):
                if idx[0] == idx[1]:
                    continue

                self.clips_to_label.append((clip_id, label))

        shuffle(self.clips_to_label)
