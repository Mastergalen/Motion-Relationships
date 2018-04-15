import unittest
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import animation

from lib.preprocessing import kinetics


class TestKinetics(unittest.TestCase):
    def test_rgb(self):
        video_path = 'data/clips/VgZW62uxRGk-450.mp4'

        kinetics.rgb(video_path)
        fig = plt.figure()

        video_data = np.load('data/kinetics/rgb_VgZW62uxRGk-450.npy')

        frames = []
        for i in range(len(video_data)):
            im = plt.imshow(video_data[i, ...], animated=True)
            frames.append([im])

        # call the animator.  blit=True means only re-draw the parts that have changed.
        anim = animation.ArtistAnimation(fig, frames, interval=300, blit=True)

        # plt.show()

