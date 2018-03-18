import numpy as np
import unittest
import lib.preprocessing.extract_vectors as extract_vectors


class TestLoader(unittest.TestCase):
    def test_extract_vectors(self):
        flow = extract_vectors.in_clip('Xbw_9hrp2KY-420')
        flow_vector = flow[0, 3, :]
        np.testing.assert_array_equal(flow_vector, [60.5,  43.5,   1.5,   0.,   0.5,   1.5])
