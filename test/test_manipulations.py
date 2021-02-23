import numpy as np
from scipy.sparse import csr_matrix
import tempfile
import pytest

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


class Test_combine_data:
    def test_combine_data_2dim(self):
        """Test that to Data instances is correctly combined with combine_data using 2 dimensional test data"""
        (
            data1,
            data1_file,
            data2,
            data2_file,
            output_file,
        ) = self._generate_test_data_2dim()

        mut.combine_data(output_file, [data1_file, data2_file])
        data_combined = combined_data.CombinedData.read(output_file)

        self.assert_ids(data1_file, data2_file, data_combined)
        assert (data_combined.data[0] == data1.data).all()
        assert (data_combined.data[1] == data2.data).all()
        assert data_combined.IDs.shape == (2,)
        assert data_combined.data.shape == (2, 3, 2)

    def test_combine_data_3dim(self):
        """Test that to Data instances is correctly combined with combine_data using 2 dimensional test data"""
        (
            data1,
            data1_file,
            data2,
            data2_file,
            output_file,
        ) = self._generate_test_data_3dim()

        mut.combine_data(output_file, [data1_file, data2_file])
        data_combined = combined_data.CombinedData.read(output_file)

        assert (data_combined.data[0] == data1.data).all()
        assert (data_combined.data[1] == data2.data).all()
        assert data_combined.IDs.shape == (2,)
        assert data_combined.data.shape == (2, 3, 2, 2)

    def test_combine_data_sparse(self):
        """Test that combine works for sparse data"""
        (
            data1,
            data1_file,
            data2,
            data2_file,
            output_file,
        ) = self._generate_sparse_test_data_3dim()

        mut.combine_data(output_file, [data1_file, data2_file])
        data_combined = combined_data.CombinedData.read(output_file)

        self.assert_sparse_data(data1, data2, data_combined)
        self.assert_ids(data1_file, data2_file, data_combined)
        assert data_combined.IDs.shape == (2,)
        assert data_combined.data.shape == (2, 3)

    def test_combine_data_wrong_data_dimensions(self):
        """Test that combine_data fails an assert when data dimensions doesn't match"""
        (
            data1,
            data1_file,
            data2,
            data2_file,
            output_file,
        ) = self._generate_test_data_2dim()
        data2 = data.Data(np.array([[40], [50], [60]]), ["chr1", "chr2", "chr3"], None)
        data2_file = _write_temp_data_file(data2)

        with pytest.raises(AssertionError):
            mut.combine_data(output_file, [data1_file, data2_file])

    def test_combine_data_region_id_mismatch(self):
        """Test that combine_data fails an assert when data region ids doesn't match"""
        (
            data1,
            data1_file,
            data2,
            data2_file,
            output_file,
        ) = self._generate_test_data_2dim()
        data2 = data.Data(
            np.array([[40, 44], [50, 55], [60, 60]]),
            ["chr1", "chr2", "WRONG_REGION_ID"],
            None,
        )
        data2_file = _write_temp_data_file(data2)

        with pytest.raises(AssertionError):
            mut.combine_data(output_file, [data1_file, data2_file])

    @staticmethod
    def _generate_test_data_2dim():
        data1 = data.Data(
            np.array([[10, 11], [20, 22], [0, 0]]), ["chr1", "chr2", "chr3"], None
        )
        data2 = data.Data(
            np.array([[40, 44], [0, 0], [60, 66]]), ["chr1", "chr2", "chr3"], None
        )
        data1_file = _write_temp_data_file(data1)
        data2_file = _write_temp_data_file(data2)
        output_file = tempfile.NamedTemporaryFile().name

        return data1, data1_file, data2, data2_file, output_file

    @staticmethod
    def _generate_test_data_3dim():
        data1 = data.Data(
            np.array(
                [
                    [[100, 101], [110, 111]],
                    [[200, 202], [220, 222]],
                    [[300, 301], [330, 3333]],
                ]
            ),
            ["chr1", "chr2", "chr3"],
            None,
        )
        data2 = data.Data(
            np.array(
                [
                    [[400, 404], [440, 444]],
                    [[500, 505], [550, 555]],
                    [[600, 606], [660, 666]],
                ]
            ),
            ["chr1", "chr2", "chr3"],
            None,
        )
        data1_file = _write_temp_data_file(data1)
        data2_file = _write_temp_data_file(data2)
        output_file = tempfile.NamedTemporaryFile().name

        return data1, data1_file, data2, data2_file, output_file

    @staticmethod
    def _generate_sparse_test_data_3dim():
        data1 = data.Data(
            np.array(
                [
                    csr_matrix([[100, 101], [110, 111]]),
                    csr_matrix([[200, 202], [220, 222]]),
                    csr_matrix([[300, 301], [330, 3333]]),
                ]
            ),
            ["chr1", "chr2", "chr3"],
            None,
        )
        data2 = data.Data(
            np.array(
                [
                    csr_matrix([[400, 404], [440, 444]]),
                    csr_matrix([[500, 505], [550, 555]]),
                    csr_matrix([[600, 606], [660, 666]]),
                ]
            ),
            ["chr1", "chr2", "chr3"],
            None,
        )
        data1_file = _write_temp_data_file(data1)
        data2_file = _write_temp_data_file(data2)
        output_file = tempfile.NamedTemporaryFile().name

        return data1, data1_file, data2, data2_file, output_file

    @staticmethod
    def assert_ids(data1_file, data2_file, data_combined):
        assert data_combined.IDs[0] == data1_file.split("/")[-1]
        assert data_combined.IDs[1] == data2_file.split("/")[-1]

    @staticmethod
    def assert_sparse_data(data1, data2, data_combined):
        assert (data_combined.data[0][0].todense() == data1.data[0].todense()).all()
        assert (data_combined.data[0][1].todense() == data1.data[1].todense()).all()
        assert (data_combined.data[0][2].todense() == data1.data[2].todense()).all()
        assert (data_combined.data[1][0].todense() == data2.data[0].todense()).all()
        assert (data_combined.data[1][1].todense() == data2.data[1].todense()).all()
        assert (data_combined.data[1][2].todense() == data2.data[2].todense()).all()


class Test_region_sum:
    def test_region_sum(self):
        data1 = data.Data(
            np.array(
                [
                    [[100, 101], [110, 111]],
                    [[200, 202], [220, 222]],
                    [[300, 301], [330, 3333]],
                ]
            ),
            ["chr1", "chr2", "chr3"],
            None,
        )
        data1_file = _write_temp_data_file(data1)
        output_file = tempfile.NamedTemporaryFile().name

        mut.region_sum(data1_file, output_file)
        data_regions_summed = data.Data.read(output_file)

        assert len(data_regions_summed.region_ids) == 1
        assert (data_regions_summed.data[0] == np.array([600, 604])).all()
        assert data_regions_summed.data.shape == (2, 2)


def _write_temp_data_file(data1):
    file = tempfile.NamedTemporaryFile().name
    data.Data.write(data1, file)
    return file
