import unittest
import numpy as np
import matplotlib.pyplot as plt

import lib.model.mask as mask


class TestMask(unittest.TestCase):
    @unittest.skip
    def test_generate_mask(self):
        img = mask.generate_mask((10, 10, 20, 20), (100, 100))

        plt.figure()
        plt.imshow(img, cmap=plt.cm.gray)
        plt.show()

    @unittest.skip
    def test_generate_mask_reversed(self):
        img = mask.generate_mask(np.array([332,  79,  82, 142]), (320, 480))

        plt.figure()
        plt.imshow(img, cmap=plt.cm.gray)
        plt.show()

    @unittest.skip
    def test_generate_mask_out_of_bounds(self):
        img = mask.generate_mask(np.array([-2, 90, 510, 43]), (320, 480))

        plt.figure()
        plt.imshow(img, cmap=plt.cm.gray)
        plt.show()
