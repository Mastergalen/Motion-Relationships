"""
Preprocessing required for the Kinetics dataset
"""
import os
import numpy as np
from moviepy.editor import *

_OUT_DIR = 'data/kinetics'
_NB_FRAMES = 150

_VIDEO_SIZE = 224


def rgb(video_path):
    """
    Preprocessing pipeline for RGB input
    :return:
    """
    if not os.path.exists(_OUT_DIR):
        os.makedirs(_OUT_DIR)

    clip_id, _ = os.path.splitext(os.path.basename(video_path))
    video = VideoFileClip(video_path)

    video = resize(video)
    video = crop(video)

    npy_path = os.path.join(_OUT_DIR, 'rgb_{}.npy'.format(clip_id))

    np_array = np.zeros((_NB_FRAMES, _VIDEO_SIZE, _VIDEO_SIZE, 3), np.float32)

    for t in range(_NB_FRAMES):
        # Rescale from -1 to 1
        np_array[t, ...] = (video.get_frame(t) / 255) - 1

    video.write_videofile(os.path.join(_OUT_DIR, "rgb_{}.mp4".format(clip_id)))

    np.save(npy_path, np_array)


def flow(video_path):
    """
    Preprocessing pipeline for flow stream input
    :return:
    """


def resize(video):
    """
    Resized so that smallest dimension is 256 pixels
    :param video:
    :return:
    """

    width, height = video.size

    if width > height:
        return video.resize(height=256)
    else:
        return video.resize(width=256)


def rescale(video):
    """
    Rescale pixel between -1 and 1
    :return:
    """


def crop(video):
    """
    224x224 center image crop
    :return:
    """
    width, height = video.size
    x_center = width / 2.0
    y_center = height / 2.0

    return video.crop(x_center=x_center, y_center=y_center, width=_VIDEO_SIZE, height=_VIDEO_SIZE)