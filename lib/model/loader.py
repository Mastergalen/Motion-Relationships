"""
Load inputs for model
"""
import json
import os
import keras
import numpy as np
from lib.model.config import CONFIG


def load():
    x_train = np.random.randn(100, 300)
    y_train = np.random.randint(0, 3, 100)

    x_valid = np.random.randn(100, 300)
    y_valid = np.random.randint(0, 3, 100)

    y_train = keras.utils.to_categorical(y_train, CONFIG['num_relationships'])
    y_valid = keras.utils.to_categorical(y_valid, CONFIG['num_relationships'])

    return x_train, y_train, x_valid, y_valid
