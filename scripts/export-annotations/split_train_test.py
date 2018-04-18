"""
Script for splitting labels into train and test set by clip_id
"""
import glob
import os
import shutil
from random import shuffle

_LABEL_DIR = 'data/labels'
_TRAIN_DIR = os.path.join(_LABEL_DIR, 'training')
_TEST_DIR = os.path.join(_LABEL_DIR, 'test')


def main():
    label_paths = glob.glob(os.path.join(_LABEL_DIR, '*.json'))

    assert len(label_paths) > 0

    shuffle(label_paths)

    split_idx = round(len(label_paths) * 0.8)

    train_paths = label_paths[:split_idx]
    test_paths = label_paths[split_idx:]

    if not os.path.exists(_TRAIN_DIR):
        os.makedirs(_TRAIN_DIR)
    if not os.path.exists(_TEST_DIR):
        os.makedirs(_TEST_DIR)

    for p in train_paths:
        file_name = os.path.basename(p)
        shutil.move(p, os.path.join(_TRAIN_DIR, file_name))

    for p in test_paths:
        file_name = os.path.basename(p)
        shutil.move(p, os.path.join(_TEST_DIR, file_name))


if __name__ == '__main__':
    main()
