import unittest
import matplotlib.pyplot as plt

from lib.utils.video import extract_frame


class TestVideo(unittest.TestCase):
    @unittest.skip
    def test_extract_frame(self):
        frame = extract_frame('data/clips/Aqko6DwEqq4-352.mp4', 11)

        plt.figure()
        plt.imshow(frame)

        # Plot green channel
        plt.figure()
        plt.imshow(frame[:, :, 1], cmap=plt.cm.gray)
        plt.show()
