import numpy as np
import logging

from ..data import Data

logger = logging.getLogger()


def region_sum(sample_file, output_file):
    """Given s sample file this function will sum the data
    across the first axis, so that all the regions are collapsed
    into one

    :param sample_file: File path to the sample file
    :type sample_file: str
    :param output_file: File path to the output file
    :type output_file: str
    """
    sample = Data.read(sample_file)
    if sample.is_sparse:
        logger.info("sample is sparse")
        result = sample.data[0]
        for matrix in sample.data[1:]:
            if matrix.count_nonzero() != 0:
                result += matrix
    else:
        logger.info("sample is dense")
        result = np.sum(sample.data, axis=0)
    Data.write(Data(result, ["region_sum"], sample.bam_report), output_file)
