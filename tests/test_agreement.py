import unittest
import numpy as np
import lib.mturk.agreement as agreement


class TestAgreement(unittest.TestCase):
    def test_merge_annotations(self):
        a = [[0, 1], [0, 4]]
        b = [[0, 2], [2, 2]]
        c = [[2, 1], [0, 4]]
        all_annotations = np.array([a, b, c])
        merged = agreement.merge_annotations(all_annotations)

        expected = np.array([[0, 1], [0, 4]])
        np.testing.assert_array_equal(merged, expected)
