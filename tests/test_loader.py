import unittest
import lib.utils.loader as loader


class TestLoader(unittest.TestCase):
    def test_load_bboxes(self):
        bboxes = loader.load_bboxes('Xbw_9hrp2KY-420')
        entity = bboxes[859]
        self.assertEqual(entity[0], (0, [69, 0, 47, 90]))
