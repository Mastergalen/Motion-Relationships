import numpy as np
import os
import json
import random
import warnings
from keras.utils import to_categorical

from lib.model.loaders import helpers
import lib.utils.loader as bbox

_DATA_DIR = 'data\\kinetics_bottleneck'
_CLIP_DIR = 'data\\clips'

_MAX_FRAMES = 150

_RESIZE_SIZE = 256
_CROP_SIZE = 224

np.random.seed(7)
random.seed(7)


class KineticsBottleneckRoiLoader:
    def __init__(self, nb_classes, dataset, frame_size=224):
        self.batch_size = 1
        self.step = 0
        self.nb_classes = nb_classes
        self.dataset = dataset
        self.frame_size = frame_size

        self.train_labels = {0: [], 1: [], 2: [], 3: [], 4: []}
        self.batches = []

        self.__load_data__()
        self.__generate_batches__()

    def load_all(self):
        nb_samples = len(self.batches)

        if self.dataset == 'training':
            # Multiply by 2 for left/right flipping
            nb_samples *= 2

        bottleneck_x = np.zeros((nb_samples, 19, 7, 7, 1024))
        roi_x = np.zeros((nb_samples, 150, 8))
        y = np.zeros(nb_samples)

        for i, batch in enumerate(self.batches):
            (clip_id, start_id, end_id), label = batch[0]
            non_flip_data = np.load(os.path.join(_DATA_DIR, '{}.npy'.format(clip_id)))[0, ...]
            if self.dataset == 'training':
                bottleneck_x[i * 2, ...] = non_flip_data
                bottleneck_x[(i * 2) + 1, ...] = np.load(os.path.join(_DATA_DIR, '{}_flip.npy'.format(clip_id)))[0, ...]
            else:
                bottleneck_x[i, ...] = non_flip_data

            # FIXME: Investigate out of range
            try:
                if self.dataset == 'training':
                    bbox_vector = self.__bbox_vector__(clip_id, start_id, end_id)
                    roi_x[i * 2, ...] = bbox_vector
                    roi_x[(i * 2) + 1, ...] = self.__flip_vector__(bbox_vector)
                else:
                    roi_x[i, ...] = self.__bbox_vector__(clip_id, start_id, end_id)
            except IndexError:
                warnings.warn('{} failed'.format(clip_id))

            # Leave out label class 1 (unsure) and shift by 1
            if label > 1:
                label -= 1

            y[i] = label

        return bottleneck_x, roi_x, to_categorical(y, self.nb_classes)

    def fetch(self):
        for batch in self.batches:
            batch_x = np.zeros((self.batch_size, _MAX_FRAMES, 224, 224, 3))
            batch_y = np.zeros((self.batch_size, self.nb_classes))

            for i in range(self.batch_size):
                clip_id, label = batch[i]
                batch_x[i, ...] = np.load(os.path.join(_DATA_DIR, '{}.npy'.format(clip_id)))
                batch_y[i, label] = 1

            yield batch_x, batch_y

    def __bbox_vector__(self, clip_id, start_id, end_id):
        bbox_path = os.path.join(_CLIP_DIR, '{}.json'.format(clip_id))
        bboxes = bbox.load_bboxes(bbox_path, _MAX_FRAMES)

        h, w = bbox.get_video_dims(bbox_path)

        smallest_dim = min(h, w)
        max_dim = max(h, w)

        scale_factor = _RESIZE_SIZE / smallest_dim
        translation = np.array([
                ((max_dim * scale_factor) - _CROP_SIZE) // 2,
                (_RESIZE_SIZE - _CROP_SIZE) // 2,
                0,  # No need to translate w and h vector again
                0
        ])

        start_boxes = bboxes[start_id]
        end_boxes = bboxes[end_id]

        start_boxes = self.__convert_vector__(start_boxes, scale_factor, translation)
        end_boxes = self.__convert_vector__(end_boxes, scale_factor, translation)

        roi_input = np.zeros((150, 8))

        for t, box in start_boxes:
            roi_input[t, 0:4] = box

        for t, box in end_boxes:
            roi_input[t, 4:8] = box

        return roi_input

    def __convert_vector__(self, boxes, scale_factor, translation):
        for i, b in enumerate(boxes):
            boxes[i] = (b[0], np.round((b[1] * scale_factor) - translation).astype(np.int32))
        return boxes

    def __generate_batches__(self):
        for i in range(2, 5):
            for clip_id in self.train_labels[i]:
                self.batches.append([(clip_id, i)])

        nb_has_relationship = len(self.batches)

        for i in range(nb_has_relationship):
            clip_id = self.train_labels[0][i]
            self.batches.append([(clip_id, 0)])

        random.shuffle(self.batches)

    def __flip_vector__(self, v):
        # Flip x coords only horizontally
        v[:, [0, 4]] = self.frame_size - v[:, [0, 4]]

        # Then subtract by the width
        v[:, 0] = v[:, 0] - v[0, 2]
        v[:, 4] = v[:, 4] - v[0, 6]

        return v

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

                self.train_labels[label].append((clip_id, idx[0], idx[1]))

        random.shuffle(self.train_labels[0])

    def __len__(self):
        return len(self.batches)