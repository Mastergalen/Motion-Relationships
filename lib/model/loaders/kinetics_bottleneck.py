import numpy as np
import os
import json
from keras.utils import to_categorical
from random import shuffle

from lib.model.loaders import helpers

_DATA_DIR = 'data\\kinetics_bottleneck'

np.random.seed(7)


class KineticsBottleneckLoader:
    def __init__(self, nb_classes, dataset, use_lr_flip):
        self.batch_size = 1
        self.step = 0
        self.nb_classes = nb_classes
        self.dataset = dataset
        self.use_lr_flip = use_lr_flip
        self.train_labels = {0: [], 1: [], 2: [], 3: [], 4: []}
        self.batches = []

        self.__load_data__()
        self.__generate_batches__()

    def load_all(self):
        nb_samples = len(self.batches)

        if self.dataset == 'training' and self.use_lr_flip:
            # Multiply by 2 for left/right flipping
            nb_samples *= 2

        x = np.zeros((nb_samples, 19, 7, 7, 1024))
        y = np.zeros(nb_samples)

        for i, batch in enumerate(self.batches):
            clip_id, label = batch[0]
            non_flip_data = np.load(os.path.join(_DATA_DIR, '{}.npy'.format(clip_id)))[0, ...]
            if self.dataset == 'training' and self.use_lr_flip:
                x[i * 2, ...] = non_flip_data
                x[(i * 2) + 1, ...] = np.load(os.path.join(_DATA_DIR, '{}_flip.npy'.format(clip_id)))[0, ...]
            else:
                x[i, ...] = non_flip_data

            # Skip label class 1 (unsure)
            if label > 1:
                label -= 1

            if self.dataset == 'training':
                y[(i*2):(i*2)+2] = label
            else:
                y[i] = label

        # Reduce to binary classification problem
        if self.nb_classes == 2:
            y[y > 0] = 1

        return x, to_categorical(y, self.nb_classes)

    def __generate_batches__(self):
        for i in range(2, 5):
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

        assert len(label_paths) > 0

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