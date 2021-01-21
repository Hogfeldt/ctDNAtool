import numpy as np
import tempfile

import ctDNAtool.manipulations as mut
import ctDNAtool.combined_data as combined_data
import ctDNAtool.data as data


class Test_stride_binning:
    def test_identity(self):
        """Test if a bin size of 1 and a stride of 1
        works as the identity function.
        """
        X = np.ones((20, 5))
        bin_size = 1
        stride = 1
        R = mut.stride_binning(X, bin_size, stride)
        assert np.array_equal(X, R) is True

    def test_binsize_eq_stride(self):
        """Test if stride and bin size are the same
        then we should just get a normal binning.
        """
        X = np.ones((20, 5))
        bin_size = 5
        stride = 5
        R = mut.stride_binning(X, bin_size, stride)
        T = np.array([5 for _ in range(4 * 5)], dtype=X.dtype).reshape((4, 5))
        assert np.array_equal(R, T) is True

    def test_stride_less_binsize(self):
        """Test with a stride less than bin size"""
        X = np.ones((20, 5))
        bin_size = 5
        stride = 2
        R = mut.stride_binning(X, bin_size, stride)
        T = np.array(
            [5 for _ in range(8 * 5)] + [4 for _ in range(5)], dtype=X.dtype
        ).reshape((9, 5))
        assert np.array_equal(R, T) is True

    def test_binsize_less_stride(self):
        """Test with a bin size less than stride"""
        X = np.ones((20, 5))
        bin_size = 1
        stride = 2
        R = mut.stride_binning(X, bin_size, stride)
        T = np.array([1 for _ in range(10 * 5)], dtype=X.dtype).reshape((10, 5))
        assert np.array_equal(R, T) is True

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
        assert np.array_equal(R, T) is True

    def test_combine_data(self):
        """Test that to Data instances is correctly combined with combine_data"""
        data1 = data.Data(np.array([1, 2, 3]), np.array(["region_id"]), None)
        data2 = data.Data(np.array([4, 5, 6]), np.array(["region_id"]), None)
        data1_file = tempfile.NamedTemporaryFile().name
        data.Data.write(data1, data1_file)
        data2_file = tempfile.NamedTemporaryFile().name
        data.Data.write(data2, data2_file)
        output_file = tempfile.NamedTemporaryFile().name

        mut.combine_data(output_file, [data1_file, data2_file])
        data_combined = combined_data.CombinedData.read(output_file)

        assert data_combined.IDs[0] == data1_file.split("/")[-1]
        assert data_combined.IDs[1] == data2_file.split("/")[-1]
        assert (data_combined.data[0].data == data1.data).all()
        assert (data_combined.data[1].data == data2.data).all()
        assert data_combined.IDs.shape == (2,)
        assert data_combined.data.shape == (2,)
