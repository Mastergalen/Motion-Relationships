import numpy as np
import unittest
from lib.utils.loader import load_bboxes
import lib.preprocessing.extract_vectors as extract_vectors


class TestExtractVectors(unittest.TestCase):
    def test_extract_vectors(self):
        bboxes = load_bboxes('data/clips/Xbw_9hrp2KY-420.json')
        flow = extract_vectors.in_clip(bboxes)
        flow_vector = flow[8, 3, :]
        np.testing.assert_array_equal(flow_vector, [ 60.5,  43.5,   1.5,   0,   0.5,   1.5],)
