import math
import numpy as np
import logging

from ..data import Data

logger = logging.getLogger()


def calc_number_of_strides(n, bin_size, stride):
    if stride <= bin_size:
        return math.ceil((n - bin_size) / stride) + 1
    else:
        return math.ceil((n - bin_size) / stride)


def stride_binning(X, bin_size, stride):
    n, m = X.shape
    n_bins = calc_number_of_strides(n, bin_size, stride)
    if (n - bin_size) % stride != 0:
        logger.warning("last bin is smaller than the given bin size")
    R = np.zeros((n_bins, m))
    for i in range(n_bins):
        start = i * stride
        end = start + bin_size
        R[i] = np.sum(X[start:end], axis=0)
    return R


def binning_update_ids(region_ids, stride, n_bins):
    return [region_ids[i * stride] for i in range(n_bins)]


def binning(sample_file, output_file, bin_size, stride):
    """This function will given a sample make an additive binning in the first axis.
    The binning is a sliding window where the bin size and a stride parameter
    can be set.

    :param sample_file: File path to the matrix/tensor
    :type sample_file:  str
    :param output_file: File path to store the result
    :type output_file:  str
    :param bin_size:    Size of the bin
    :type bin_size:     Integer
    :param stride:      The step size of the sliding window
    :type stride:       Integer
    """
    # TODO: Also implement for sparse tensors or ndarray containing scipy sparse matrices
    sample = Data.read(sample_file)
    R = stride_binning(sample.data, bin_size, stride)
    new_region_ids = binning_update_ids(sample.region_ids, stride, R.shape[0])
    Data.write(Data(R, new_region_ids, sample.bam_report), output_file)
