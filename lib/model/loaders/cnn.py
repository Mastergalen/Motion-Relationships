import numpy as np
import os
import json
from keras.utils import to_categorical
from random import shuffle

from lib.model.loaders import helpers

np.random.seed(7)


class CnnLoader:
    def __init__(self, nb_classes, dataset):
        self.batch_size = 1
        self.step = 0
        self.nb_classes = nb_classes
        self.dataset = dataset
        self.train_labels = {0: [], 1: [], 2: [], 3: [], 4: []}
        self.batches = []

        self.__load_data__()
        self.__generate_batches__()

    def __generate_batches__(self):
        for i in range(2, 5):
            for clip_id, idx_pair in self.train_labels[i]:
                # Subtract i by 1 to ignore "unsure" class
                self.batches.append((clip_id, idx_pair, i-1))

        nb_has_relationship = len(self.batches)

        for i in range(nb_has_relationship):
            clip_id, idx_pair = self.train_labels[0][i]
            self.batches.append((clip_id, idx_pair, 0))

        shuffle(self.batches)

    def __load_data__(self):
        """
        (clip_id, class_id)
        :return:
        """
        label_paths = helpers.list_labels(self.dataset)

        assert len(label_paths) > 0

        for path in label_paths:
            clip_id = os.path.splitext(os.path.basename(path))[0]
            labels = np.array(json.load(open(path)))

            for idx, label in np.ndenumerate(labels):
                if idx[0] == idx[1]:
                    continue

                self.train_labels[label].append((clip_id, idx))

        shuffle(self.train_labels[0])

    def __len__(self):
        return len(self.batches)