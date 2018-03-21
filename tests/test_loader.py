import unittest
import numpy as np
import lib.utils.loader as loader


class TestLoader(unittest.TestCase):
    def test_load_bboxes(self):
        bboxes = loader.load_bboxes('data/clips/Xbw_9hrp2KY-420.json')
        entity = bboxes[8]  # Entity ID = 859
        self.assertEqual(0, entity[0][0])
        np.testing.assert_array_equal(entity[0][1], [69, 0, 47, 90])
