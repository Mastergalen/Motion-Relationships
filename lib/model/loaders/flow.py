"""
Load inputs for flow vector based model
"""
import json
import os
import keras
import numpy as np

from lib.model.config import CONFIG
from lib.model.loaders.helpers import list_labels


def load():
    x, y = read_files()
    examples = len(y)
    # TODO: Unison shuffle
    print("Total labels: {}".format(examples))

    split_idx = round(examples * CONFIG['split'])

    x_train = x[:split_idx, :, :]
    y_train = y[:split_idx]

    x_valid = x[split_idx:, :, :]
    y_valid = y[split_idx:]

    y_train = keras.utils.to_categorical(y_train, CONFIG['num_relationships'])
    y_valid = keras.utils.to_categorical(y_valid, CONFIG['num_relationships'])

    return x_train, y_train, x_valid, y_valid


def read_files():
    label_files = list_labels()

    x = np.zeros((0, CONFIG['frames'] * 2, 6))
    y = np.zeros(0)
    for path in label_files:
        file_name = os.path.basename(path)

        flow_path = os.path.join(CONFIG['data_dir'], 'flows', file_name)
        with open(flow_path) as fp:
            data = np.array(json.load(fp))

            rows, cols = np.indices((data.shape[0], data.shape[0]))
            xs, ys = np.vstack([rows.ravel(), cols.ravel()])

            a = data[xs, :, :]
            b = data[ys, :, :]

            product = np.concatenate((a, b), axis=1)
            x = np.append(x, product, axis=0)

        with open(path) as fp:
            labels = np.array(json.load(fp))
            y = np.append(y, labels.flatten())

    return x, y
