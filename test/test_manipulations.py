import unittest
from unittest import TestCase
import numpy as np

import ctDNAtool.manipulations as mut


class Test_stride_binning(TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_identity(self):
        """Test if a bin size of 1 and a stride of 1
        works as the identity function.
        """
        X = np.ones((20, 5))
        bin_size = 1
        stride = 1
        R = mut.stride_binning(X, bin_size, stride)
        self.assertTrue(np.array_equal(X, R))

    def test_binsize_eq_stride(self):
        """Test if stride and bin size are the same
        then we should just get a normal binning.
        """
        X = np.ones((20, 5))
        bin_size = 5
        stride = 5
        R = mut.stride_binning(X, bin_size, stride)
        T = np.array([5 for _ in range(4 * 5)], dtype=X.dtype).reshape((4, 5))
        self.assertTrue(np.array_equal(R, T))

    def test_stride_less_binsize(self):
        """Test with a stride less than bin size"""
        X = np.ones((20, 5))
        bin_size = 5
        stride = 2
        R = mut.stride_binning(X, bin_size, stride)
        T = np.array(
            [5 for _ in range(8 * 5)] + [4 for _ in range(5)], dtype=X.dtype
        ).reshape((9, 5))
        self.assertTrue(np.array_equal(R, T))

    def test_binsize_less_stride(self):
        """Test with a bin size less than stride"""
        X = np.ones((20, 5))
        bin_size = 1
        stride = 2
        R = mut.stride_binning(X, bin_size, stride)
        T = np.array([1 for _ in range(10 * 5)], dtype=X.dtype).reshape((10, 5))
        # print(R)
        # print(T)
        self.assertTrue(np.array_equal(R, T))

    def test_last_bin_exceeds_array(self):
        """Test when the last bin exceeds the
        length of the matrice dim 0 length.
        The last bin should be smaller than
        the rest of the bins.
        """
        X = np.ones((15, 5))
        bin_size = 5
        stride = 3
        R = mut.stride_binning(X, bin_size, stride)
        T = np.array(
            [5 for _ in range(4 * 5)] + [3 for _ in range(5)], dtype=X.dtype
        ).reshape((5, 5))
        self.assertTrue(np.array_equal(R, T))


if __name__ == "__main__":
    unittest.main()
