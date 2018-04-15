"""
Run preprocessing for all video clips for the pre-trained Kinetics i3d model
"""
import os
import glob
import progressbar
import tensorflow as tf

from lib.preprocessing import kinetics

_INPUT_VIDEOS_DIR = 'data/clips'
_OUT_DIR = 'data/kinetics'


def main():
    if not os.path.exists(_OUT_DIR):
        os.makedirs(_OUT_DIR)

    vid_paths = glob.glob("{}/*.mp4".format(_INPUT_VIDEOS_DIR))

    bar = progressbar.ProgressBar()
    for p in bar(vid_paths):
        kinetics.rgb(p)


if __name__ == '__main__':
    main()
