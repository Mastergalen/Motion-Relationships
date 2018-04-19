import numpy as np
import os
import json
from random import shuffle

from lib.model.loaders import helpers

_DATA_DIR = 'data/kinetics'

np.random.seed(7)


class KineticsLoader:
    def __init__(self, batch_size, nb_classes, dataset):
        self.batch_size = batch_size
        self.step = 0
        self.nb_classes = nb_classes
        self.dataset = dataset
        self.train_labels = {0: [], 1: [], 2: [], 3: [], 4: []}
        self.batches = []

        self.__load_data__()
        self.__generate_batches__()

    def next_batch(self):
        batch_x = np.zeros((self.batch_size, 150, 224, 224, 3))
        batch_y = np.zeros((self.batch_size, self.nb_classes))

        batch = self.batches[self.step % len(self.batches)]
        for i in range(self.batch_size):
            clip_id, label = batch[i]
            batch_x[i, ...] = np.load(os.path.join(_DATA_DIR, 'rgb_{}.npy'.format(clip_id)))
            batch_y[i, label] = 1

        self.step += 1

        return batch_x, batch_y

    def __generate_batches__(self):
        for i in range(1, 5):
            for clip_id in self.train_labels[i]:
                self.batches.append([(clip_id, i)])

        nb_has_relationship = len(self.batches)

        for i in range(nb_has_relationship):
            clip_id = self.train_labels[0][i]
            self.batches.append([(clip_id, 0)])

        shuffle(self.batches)

    def __load_data__(self):
        """
        (clip_id, class_id)
        :return:
        """
        label_paths = helpers.list_labels(self.dataset)

        for path in label_paths:
            clip_id = os.path.splitext(os.path.basename(path))[0]
            labels = np.array(json.load(open(path)))

            for idx, label in np.ndenumerate(labels):
                if idx[0] == idx[1]:
                    continue

                self.train_labels[label].append(clip_id)

        shuffle(self.train_labels[0])

    def __len__(self):
        return len(self.batches)